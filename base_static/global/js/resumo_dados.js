document.addEventListener('DOMContentLoaded', function () {
    // Buscar os dados via API
    fetch('api/resumo-dados/')
        .then(response => response.json())
        .then(data => {
            const receitas = data.resumo_receitas;
            const despesas = data.resumo_despesas;

            // Dados para o gráfico de receitas
            const labelsReceitas = receitas.map(r => r["Nome da Transação"]);
            const valoresReceitas = receitas.map(r => r["Receita"]);

            // Dados para o gráfico de despesas
            const labelsDespesas = despesas.map(r => r["Nome da Transação"]);
            const valoresDespesas = despesas.map(r => r["Despesa"]);

            // Recuperar o contexto do canvas
            var ctxReceitas = document.getElementById('grafico-receitas').getContext('2d');
            var ctxDespesas = document.getElementById('grafico-despesas').getContext('2d');

            // Configuração do gráfico de receitas
            var graficoReceitas = new Chart(ctxReceitas, {
                type: 'bar', // tipo do gráfico (linha)
                data: {
                    labels: labelsReceitas, // Labels dinâmicas baseadas nos dados da API
                    datasets: [{
                        label: 'Receitas',
                        data: valoresReceitas, // Dados dinâmicos de receitas
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Configuração do gráfico de despesas
            var graficoDespesas = new Chart(ctxDespesas, {
                type: 'bar', // tipo do gráfico (barras)
                data: {
                    labels: labelsDespesas, // Labels dinâmicas baseadas nos dados da API
                    datasets: [{
                        label: 'Despesas',
                        data: valoresDespesas, // Dados dinâmicos de despesas
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erro ao buscar dados da API:', error);
        });
});
