const alvo = document.getElementById('alvo');
const tempoReacao = document.getElementById('tempo-reacao');
const pontuacao = document.getElementById('pontuacao');
const iniciarBtn = document.getElementById('iniciar');
const instrucao = document.getElementById('instrucao');
const container = document.querySelector('.container');

let inicioTempo;
let cliques = 0;
let jogoAtivo = false;
const tempoAparecer = 720;

function iniciarJogo() {
    cliques = 0;
    pontuacao.textContent = 'Cliques: 0';
    tempoReacao.textContent = 'Tempo de reação: 0.00s';
    instrucao.textContent = 'Clique no círculo antes que ele desapareça!';
    iniciarBtn.style.display = 'none';
    jogoAtivo = true;
    moverAlvo();
}

function moverAlvo() {
    if (!jogoAtivo) return;

    const containerRect = container.getBoundingClientRect();
    const alvoSize = 60;

    const x = Math.random() * (containerRect.width - alvoSize);
    const y = Math.random() * (containerRect.height - alvoSize);

    alvo.style.width = `${alvoSize}px`;
    alvo.style.height = `${alvoSize}px`;
    alvo.style.left = `${x}px`;
    alvo.style.top = `${y}px`;
    alvo.style.display = 'block';

    inicioTempo = new Date().getTime();

    setTimeout(() => {
        if (alvo.style.display === 'block') {
            alvo.style.display = 'none';
            if (jogoAtivo) {
                setTimeout(moverAlvo, 1000);
            }
        }
    }, tempoAparecer);
}

function cliqueAlvo() {
    const fimTempo = new Date().getTime();
    const tempo = (fimTempo - inicioTempo) / 1000;
    tempoReacao.textContent = `Tempo de reação: ${tempo.toFixed(2)}s`;
    cliques++;
    pontuacao.textContent = `Cliques: ${cliques}`;
    alvo.style.display = 'none';
    if (jogoAtivo) {
        setTimeout(moverAlvo, 1000);
    }
}

function terminarJogo() {
    jogoAtivo = false;
    alvo.style.display = 'none';
    iniciarBtn.style.display = 'block';
    instrucao.textContent = 'Jogo terminado! Clique em "Iniciar Jogo" para jogar novamente.';
}

alvo.addEventListener('click', cliqueAlvo);
iniciarBtn.addEventListener('click', iniciarJogo);

setTimeout(terminarJogo, 30000);
