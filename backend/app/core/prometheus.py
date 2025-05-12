from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

# Métricas personalizadas
VOTOS_TOTAL = Counter(
    "votos_total",
    "Total de votos registrados",
    ["participante_id"]
)

TEMPO_RESPOSTA = Histogram(
    "tempo_resposta_segundos",
    "Tempo de resposta da API em segundos",
    ["endpoint"]
)

ERROS_TOTAL = Counter(
    "erros_total",
    "Total de erros na aplicação",
    ["tipo_erro"]
)


def setup_prometheus(app):
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="fastapi_inprogress",
        inprogress_labels=True,
    )

    # Adiciona métricas padrão
    instrumentator.add(metrics.default())

    # Adiciona métricas personalizadas
    def custom_metrics(info: Info) -> None:
        # Métricas de tempo de resposta
        TEMPO_RESPOSTA.labels(endpoint=info.modified_handler).observe(info.modified_duration)
        
        # Métricas de erros
        if info.modified_status >= 400:
            ERROS_TOTAL.labels(tipo_erro=str(info.modified_status)).inc()

    instrumentator.add(custom_metrics)
    
    # Instrumenta a aplicação
    instrumentator.instrument(app).expose(app) 