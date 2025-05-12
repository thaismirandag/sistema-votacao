import React, { useState, useEffect } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';
import axios from 'axios';
import styled from 'styled-components';

interface Participante {
  id: string;
  nome: string;
  foto_url: string;
  total_votos: number;
  percentual: number;
}

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100vh;
`;

const Titulo = styled.h1`
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-size: 2.5rem;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const Card = styled.div<{ selected?: boolean }>`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 3px solid ${props => props.selected ? '#4CAF50' : 'transparent'};

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
  }
`;

const Foto = styled.img`
  width: 250px;
  height: 250px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1.5rem;
  border: 4px solid #f0f0f0;
  transition: border-color 0.3s ease;

  ${Card}:hover & {
    border-color: #4CAF50;
  }
`;

const Nome = styled.h2`
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #333;
`;

const Votos = styled.div`
  font-size: 1.4rem;
  color: #666;
  margin-top: 1rem;
  padding: 0.5rem;
  background: #f8f8f8;
  border-radius: 8px;
`;

const Percentual = styled.div`
  font-size: 2rem;
  color: #4CAF50;
  font-weight: bold;
  margin-top: 0.5rem;
`;

const CaptchaContainer = styled.div`
  display: flex;
  justify-content: center;
  margin: 2rem 0;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const BotaoVotar = styled.button`
  background: #4CAF50;
  color: white;
  border: none;
  padding: 1.2rem 3rem;
  border-radius: 8px;
  font-size: 1.4rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: block;
  margin: 0 auto;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
  }

  &:hover:not(:disabled) {
    background: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
`;

const Mensagem = styled.div`
  text-align: center;
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1.2rem;

  &.sucesso {
    background: #e8f5e9;
    color: #2e7d32;
  }

  &.erro {
    background: #ffebee;
    color: #c62828;
  }
`;

const RECAPTCHA_SITE_KEY = process.env.REACT_APP_RECAPTCHA_SITE_KEY;
const API_URL = process.env.REACT_APP_API_URL;

// Debug temporário
console.log('RECAPTCHA_SITE_KEY:', RECAPTCHA_SITE_KEY);

const ParedaoVotacao: React.FC = () => {
  const [participantes, setParticipantes] = useState<Participante[]>([]);
  const [participanteSelecionado, setParticipanteSelecionado] = useState<string | null>(null);
  const [captchaToken, setCaptchaToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState<{ texto: string; tipo: 'sucesso' | 'erro' | null }>({ texto: '', tipo: null });

  useEffect(() => {
    carregarParticipantes();
  }, []);

  const carregarParticipantes = async () => {
    try {
      const response = await axios.get(`${API_URL}/participantes`);
      setParticipantes(response.data);
    } catch (error) {
      console.error('Erro ao carregar participantes:', error);
      setMensagem({ texto: 'Erro ao carregar participantes. Tente novamente.', tipo: 'erro' });
    }
  };

  const handleVotar = async () => {
    if (!participanteSelecionado || !captchaToken) return;

    setLoading(true);
    setMensagem({ texto: '', tipo: null });

    try {
      await axios.post(`${API_URL}/votos`, {
        participante_id: participanteSelecionado,
        captcha_token: captchaToken
      });
      
      await carregarParticipantes();
      setParticipanteSelecionado(null);
      setCaptchaToken(null);
      setMensagem({ texto: 'Voto registrado com sucesso!', tipo: 'sucesso' });
    } catch (error) {
      console.error('Erro ao votar:', error);
      setMensagem({ texto: 'Erro ao registrar voto. Tente novamente.', tipo: 'erro' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Titulo>Paredão BBB</Titulo>
      
      {mensagem.tipo && (
        <Mensagem className={mensagem.tipo}>
          {mensagem.texto}
        </Mensagem>
      )}

      <Grid>
        {participantes.map((participante) => (
          <Card
            key={participante.id}
            selected={participanteSelecionado === participante.id}
            onClick={() => setParticipanteSelecionado(participante.id)}
          >
            <Foto src={participante.foto_url} alt={participante.nome} />
            <Nome>{participante.nome}</Nome>
            <Votos>
              {participante.total_votos} votos
              <Percentual>{participante.percentual.toFixed(1)}%</Percentual>
            </Votos>
          </Card>
        ))}
      </Grid>

      <CaptchaContainer>
        <ReCAPTCHA
          sitekey={RECAPTCHA_SITE_KEY || ''}
          onChange={(token: string | null) => setCaptchaToken(token)}
          theme="light"
          size="normal"
        />
      </CaptchaContainer>

      <BotaoVotar
        onClick={handleVotar}
        disabled={!participanteSelecionado || !captchaToken || loading}
      >
        {loading ? 'Registrando voto...' : 'Votar'}
      </BotaoVotar>
    </Container>
  );
};

export default ParedaoVotacao; 