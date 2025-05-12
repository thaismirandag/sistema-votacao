from prometheus_client import Counter, Histogram, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
from fastapi import Response

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
        env_var_name="ENABLE_METRICS",
        inprogress_name="fastapi_inprogress",
        inprogress_labels=True,
    )

    instrumentator.add(metrics.default())

    def custom_metrics(info: Info) -> None:
        TEMPO_RESPOSTA.labels(endpoint=info.modified_handler).observe(info.modified_duration)

        if info.modified_status >= 400:
            ERROS_TOTAL.labels(tipo_erro=str(info.modified_status)).inc()

    instrumentator.add(custom_metrics)

    instrumentator.instrument(app)

    @app.get("/metrics")
    async def metrics_endpoint():
        return Response(generate_latest(), media_type="text/plain")
