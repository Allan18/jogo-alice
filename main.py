# Autor/Desenvolvedor: Allan Daniel 
import pygame
import sys
import math
import random

pygame.init()

# Sons do Jogo
pygame.mixer.music.load("trilha-sonora.mp3")
pygame.mixer.music.play(-1)

# Tela do Jogo
LARGURA, ALTURA = 900, 550
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Alice vs Rainha de Copas")
clock = pygame.time.Clock()

#Paleta de Cor
COR = {
    "fundo_ceu": (20, 10, 40),
    "fundo_chao": (10, 60, 20),
    "alice_corpo": (100, 160, 220),
    "alice_avental": (240, 240, 240),
    "alice_cabelo": (220, 180, 80),
    "rainha_corpo": (160, 0, 40),
    "rainha_coroa": (220, 180, 0),
    "rainha_cara": (240, 200, 180),
    "hp_alice": (80, 180, 255),
    "hp_rainha": (220, 30, 60),
    "hp_bg": (40, 20, 20),
    "texto": (255, 240, 200),
    "amarelo": (255, 220, 0),
    "preto": (0, 0, 0),
    "branco": (255, 255, 255),
    "rosa": (255, 100, 150),
    "verde": (50, 200, 80),
    "card_vm": (200, 0, 30),
    "card_bg": (245, 235, 210),
}

#Fontes
fonte_titulo = pygame.font.SysFont("Georgia", 42, bold=True)
fonte_grande = pygame.font.SysFont("Georgia", 28, bold=True)
fonte_media = pygame.font.SysFont("Arial", 22)
fonte_pequena = pygame.font.SysFont("Arial", 16)

#Arte dos Personagens
def _coração(surf, cx, cy, r, cor):
    pts = []
    for ang in range(0, 360, 6):
        a = math.radians(ang)
        x = r * 16 * (math.sin(a) ** 3)
        y = -r * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x // 10, cy + y // 10))
    if len(pts) >= 3:
        pygame.draw.polygon(surf, cor, pts)


def _coroa(surf, cx, cy, s):
    base_y = int(cy + 10 * s)
    pygame.draw.rect(surf, COR["rainha_coroa"], (int(cx - 26 * s), base_y, int(52 * s), int(18 * s)))
    for dx in (-20, -8, 4, 16):
        pygame.draw.polygon(surf, COR["rainha_coroa"], [
            (int(cx + dx * s), base_y),
            (int(cx + (dx + 6) * s), int(cy - 8 * s)),
            (int(cx + (dx + 12) * s), base_y),
        ])
    for dx in (-16, -4, 8, 20):
        pygame.draw.circle(surf, COR["card_vm"], (int(cx + dx * s), int(cy + 18 * s)), max(1, int(4 * s)))


def desenhar_alice(surf, cx, cy, escala=1.0, piscando=False):
    s = escala
    pygame.draw.ellipse(surf, COR["alice_corpo"], (int(cx - 30 * s), int(cy + 20 * s), int(60 * s), int(70 * s)))
    pygame.draw.ellipse(surf, COR["alice_avental"], (int(cx - 18 * s), int(cy + 25 * s), int(36 * s), int(60 * s)))
    pygame.draw.rect(surf, COR["alice_corpo"], (int(cx - 20 * s), int(cy - 30 * s), int(40 * s), int(55 * s)), border_radius=8)
    pygame.draw.rect(surf, COR["alice_avental"], (int(cx - 12 * s), int(cy - 28 * s), int(24 * s), int(52 * s)), border_radius=6)
    pygame.draw.ellipse(surf, (240, 200, 180), (int(cx - 22 * s), int(cy - 75 * s), int(44 * s), int(50 * s)))
    pygame.draw.ellipse(surf, COR["alice_cabelo"], (int(cx - 26 * s), int(cy - 80 * s), int(52 * s), int(35 * s)))
    pygame.draw.rect(surf, COR["alice_cabelo"], (int(cx - 26 * s), int(cy - 68 * s), int(10 * s), int(28 * s)), border_radius=4)
    pygame.draw.rect(surf, COR["alice_cabelo"], (int(cx + 16 * s), int(cy - 68 * s), int(10 * s), int(28 * s)), border_radius=4)
    pygame.draw.polygon(surf, COR["alice_corpo"], [(int(cx - 22 * s), int(cy - 82 * s)), (int(cx - 6 * s), int(cy - 76 * s)), (int(cx - 14 * s), int(cy - 70 * s))])
    pygame.draw.polygon(surf, COR["alice_corpo"], [(int(cx + 22 * s), int(cy - 82 * s)), (int(cx + 6 * s), int(cy - 76 * s)), (int(cx + 14 * s), int(cy - 70 * s))])
    if not piscando:
        pygame.draw.ellipse(surf, COR["preto"], (int(cx - 14 * s), int(cy - 58 * s), int(10 * s), int(12 * s)))
        pygame.draw.ellipse(surf, COR["preto"], (int(cx + 4 * s), int(cy - 58 * s), int(10 * s), int(12 * s)))
        pygame.draw.circle(surf, COR["branco"], (int(cx - 10 * s), int(cy - 54 * s)), max(1, int(3 * s)))
        pygame.draw.circle(surf, COR["branco"], (int(cx + 8 * s), int(cy - 54 * s)), max(1, int(3 * s)))
    else:
        pygame.draw.line(surf, COR["preto"], (int(cx - 14 * s), int(cy - 52 * s)), (int(cx - 4 * s), int(cy - 52 * s)), 2)
        pygame.draw.line(surf, COR["preto"], (int(cx + 4 * s), int(cy - 52 * s)), (int(cx + 14 * s), int(cy - 52 * s)), 2)
    pygame.draw.arc(surf, (180, 80, 80), (int(cx - 10 * s), int(cy - 47 * s), int(20 * s), int(14 * s)), math.pi, 2 * math.pi, 2)
    pygame.draw.line(surf, (240, 200, 180), (int(cx - 20 * s), int(cy - 20 * s)), (int(cx - 45 * s), int(cy + 5 * s)), max(1, int(7 * s)))
    pygame.draw.line(surf, (240, 200, 180), (int(cx + 20 * s), int(cy - 20 * s)), (int(cx + 45 * s), int(cy + 5 * s)), max(1, int(7 * s)))
    pygame.draw.rect(surf, (240, 200, 180), (int(cx - 18 * s), int(cy + 80 * s), int(12 * s), int(30 * s)), border_radius=4)
    pygame.draw.rect(surf, (240, 200, 180), (int(cx + 6 * s), int(cy + 80 * s), int(12 * s), int(30 * s)), border_radius=4)
    pygame.draw.ellipse(surf, COR["preto"], (int(cx - 22 * s), int(cy + 106 * s), int(20 * s), int(10 * s)))
    pygame.draw.ellipse(surf, COR["preto"], (int(cx + 2 * s), int(cy + 106 * s), int(20 * s), int(10 * s)))


def desenhar_rainha(surf, cx, cy, escala=1.0, raiva=False):
    s = escala
    pygame.draw.ellipse(surf, COR["rainha_corpo"], (int(cx - 45 * s), int(cy + 10 * s), int(90 * s), int(90 * s)))
    pygame.draw.rect(surf, COR["rainha_corpo"], (int(cx - 25 * s), int(cy - 40 * s), int(50 * s), int(55 * s)), border_radius=6)
    _coração(surf, int(cx), int(cy - 18 * s), max(1, int(12 * s)), COR["rainha_coroa"])
    pygame.draw.ellipse(surf, COR["rainha_cara"], (int(cx - 24 * s), int(cy - 90 * s), int(48 * s), int(56 * s)))
    _coroa(surf, cx, cy - 90 * s, s)
    eye_col = (200, 0, 0) if raiva else COR["preto"]
    pygame.draw.ellipse(surf, eye_col, (int(cx - 16 * s), int(cy - 72 * s), int(10 * s), int(13 * s)))
    pygame.draw.ellipse(surf, eye_col, (int(cx + 6 * s), int(cy - 72 * s), int(10 * s), int(13 * s)))
    if raiva:
        pygame.draw.line(surf, COR["preto"], (int(cx - 18 * s), int(cy - 78 * s)), (int(cx - 6 * s), int(cy - 74 * s)), 3)
        pygame.draw.line(surf, COR["preto"], (int(cx + 8 * s), int(cy - 74 * s)), (int(cx + 20 * s), int(cy - 78 * s)), 3)
        pygame.draw.line(surf, (100, 0, 0), (int(cx - 12 * s), int(cy - 55 * s)), (int(cx + 12 * s), int(cy - 55 * s)), 3)
    else:
        pygame.draw.arc(surf, (150, 50, 50), (int(cx - 10 * s), int(cy - 60 * s), int(20 * s), int(12 * s)), math.pi, 2 * math.pi, 2)
    pygame.draw.line(surf, COR["rainha_cara"], (int(cx - 25 * s), int(cy - 25 * s)), (int(cx - 55 * s), int(cy + 10 * s)), max(1, int(8 * s)))
    pygame.draw.line(surf, COR["rainha_cara"], (int(cx + 25 * s), int(cy - 25 * s)), (int(cx + 55 * s), int(cy + 10 * s)), max(1, int(8 * s)))
    pygame.draw.line(surf, COR["rainha_coroa"], (int(cx + 55 * s), int(cy + 10 * s)), (int(cx + 60 * s), int(cy - 40 * s)), 4)
    _coração(surf, int(cx + 60 * s), int(cy - 46 * s), max(1, int(10 * s)), COR["card_vm"])
    pygame.draw.rect(surf, COR["rainha_cara"], (int(cx - 18 * s), int(cy + 90 * s), int(14 * s), int(25 * s)), border_radius=4)
    pygame.draw.rect(surf, COR["rainha_cara"], (int(cx + 4 * s), int(cy + 90 * s), int(14 * s), int(25 * s)), border_radius=4)
    pygame.draw.ellipse(surf, COR["preto"], (int(cx - 22 * s), int(cy + 112 * s), int(22 * s), int(10 * s)))
    pygame.draw.ellipse(surf, COR["preto"], (int(cx + 0 * s), int(cy + 112 * s), int(22 * s), int(10 * s)))


def desenhar_fundo(t):
    for y in range(ALTURA * 2 // 3):
        prog = y / (ALTURA * 2 / 3)
        r = int(20 + 60 * prog)
        g = int(10 + 20 * prog)
        b = int(40 + 40 * prog)
        pygame.draw.line(tela, (r, g, b), (0, y), (LARGURA, y))
    random.seed(42)
    for _ in range(40):
        sx = random.randint(0, LARGURA)
        sy = random.randint(0, ALTURA // 3)
        br = int(180 + 70 * math.sin(t * 2 + sx))
        pygame.draw.circle(tela, (br, br, br), (sx, sy), 1)
    chao_y = ALTURA * 2 // 3
    for y in range(chao_y, ALTURA, 24):
        for x in range(0, LARGURA, 24):
            cor = COR["verde"] if ((x // 24 + y // 24) % 2 == 0) else (30, 120, 50)
            pygame.draw.rect(tela, cor, (x, y, 24, 24))
    for torre in (200, 650, 450):
        pygame.draw.rect(tela, (60, 10, 10), (torre - 20, chao_y - 120, 40, 120))
        pygame.draw.polygon(tela, (80, 10, 10), [(torre - 24, chao_y - 120), (torre, chao_y - 155), (torre + 24, chao_y - 120)])
        for dx in (-16, -6, 4, 14):
            pygame.draw.rect(tela, (80, 10, 10), (torre + dx, chao_y - 128, 6, 10))
    for i in range(8):
        rx = 80 + i * 105
        ry = chao_y - 30 + int(6 * math.sin(t * 1.5 + i))
        _coração(tela, rx, ry, 8, COR["card_vm"])
    for i in range(5):
        cx = int((100 + i * 160 + 30 * math.sin(t + i * 1.3)) % LARGURA)
        cy = int(chao_y - 80 + 20 * math.cos(t * 0.8 + i))
        ang = math.sin(t + i) * 30
        _carta_voando(tela, cx, cy, ang)


def _carta_voando(surf, cx, cy, angulo_deg):
    w, h = 22, 30
    surf2 = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf2, COR["card_bg"], (0, 0, w, h), border_radius=3)
    pygame.draw.rect(surf2, (180, 160, 130), (0, 0, w, h), 1, border_radius=3)
    _coração(surf2, w // 2, h // 2, 5, COR["card_vm"])
    rot = pygame.transform.rotate(surf2, angulo_deg)
    surf.blit(rot, (cx - rot.get_width() // 2, cy - rot.get_height() // 2))


#Efeito do Ataque
class Particula:
    def __init__(self, x, y, cor, vel=None):
        self.x, self.y = float(x), float(y)
        self.cor = cor
        ang = random.uniform(0, 2 * math.pi)
        v = random.uniform(1, 5) if vel is None else vel
        self.vx = math.cos(ang) * v
        self.vy = math.sin(ang) * v - random.uniform(1, 3)
        self.vida = random.randint(20, 50)
        self.r = random.randint(3, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15
        self.vida -= 1

    def draw(self, surf):
        alpha = max(0, self.vida * 5)
        s = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, min(255, alpha)), (self.r, self.r), self.r)
        surf.blit(s, (int(self.x - self.r), int(self.y - self.r)))


particulas = []


def explodir(x, y, cor, n=30):
    for _ in range(n):
        particulas.append(Particula(x, y, cor))


def barra_hp(x, y, w, h, pct, cor_hp, nome):
    pct = max(0.0, min(1.0, pct))
    pygame.draw.rect(tela, COR["rainha_coroa"], (x - 3, y - 3, w + 6, h + 6), border_radius=6)
    pygame.draw.rect(tela, COR["hp_bg"], (x, y, w, h), border_radius=4)
    if pct > 0:
        pygame.draw.rect(tela, cor_hp, (x, y, int(w * pct), h), border_radius=4)
    pygame.draw.rect(tela, (255, 255, 255, 60), (x, y, int(w * pct), h // 3), border_radius=4)
    lbl = fonte_pequena.render(f"{nome} {int(pct * 100)}%", True, COR["texto"])
    tela.blit(lbl, (x, y - 20))


#Tela de Introdução
def mostrar_introducao():
    aguardando = True
    while aguardando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                aguardando = False

        tela.fill(COR["fundo_ceu"])
        desenhar_fundo(0)

        painel = pygame.Surface((LARGURA - 140, 220), pygame.SRCALPHA)
        painel.fill((10, 5, 25, 200))
        tela.blit(painel, (70, 120))

        titulo = fonte_titulo.render("*** Alice vs Rainha de Copas ***", True, COR["amarelo"])
        texto1 = fonte_media.render("Aluno: Allan Daniel RU: 5253349", True, COR["texto"])
        texto2 = fonte_pequena.render("[ ESPAÇO ] Atacar [ R ] Reinicia [ ESC ] Sair", True, (210, 200, 180))

        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 165))
        tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, 235))
        tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, 275))

        pygame.display.flip()
        clock.tick(30)

#Classe Principal do Jogo
class Jogo:
    def __init__(self):
        self.hp_alice = 1.0
        self.hp_rainha = 1.0
        self.mensagem = "MDS Ajude Alice a se libertar da Rainha de Copas!"
        self.sub_msg = ""
        self.estado = "jogando"
        self.t = 0.0
        self.piscar = False
        self.piscar_t = 0
        self.rainha_raiva = False
        self.shake = 0
        self.flash_cor = None
        self.flash_t = 0
        self.alice_x = 220
        self.rainha_x = 660
        self.alice_anim = 0.0
        self.rainha_anim = 0.0

    def atacar(self):
        if self.estado != "jogando":
            return

        dano_alice = random.uniform(0.08, 0.15)
        self.hp_rainha -= dano_alice
        explodir(self.rainha_x, 260, COR["rosa"], 25)
        self.shake = 8
        self.flash_cor = (255, 100, 100)
        self.flash_t = 8
        self.rainha_raiva = True

        self.mensagem = random.choice([
            "Alice usou Cogumelos Magicos...",
            "Alice avançou com coragem!",
            "Alice atacou a Rainha!",
        ])

        if self.hp_rainha <= 0:
            self.hp_rainha = 0
            self.estado = "vitoria"
            self.mensagem = "Obrigado por libertar Alice..."
            self.sub_msg = "Pressione R para jogar de novo"
            explodir(self.rainha_x, 250, COR["amarelo"], 60)
            explodir(LARGURA // 2, ALTURA // 2, COR["rosa"], 60)
            return

        dano_rainha = random.uniform(0.05, 0.12)
        self.hp_alice -= dano_rainha
        explodir(self.alice_x, 260, COR["card_vm"], 20)
        self.sub_msg = random.choice([
            "Rainha gritou 'Cortem-lhe a cabeça!!!'",
            "Rainha lançou cartas afiadas!",
            "Rainha contra-atacou com furia!",
        ])

        if self.hp_alice <= 0:
            self.hp_alice = 0
            self.estado = "derrota"
            self.mensagem = "Derrota... Alice foi capturada!"
            self.sub_msg = "Pressione R para tentar de novo"
            explodir(self.alice_x, 250, COR["preto"], 40)

    def reiniciar(self):
        self.__init__()

    def update(self):
        self.t += 0.03
        self.alice_anim = math.sin(self.t * 2) * 4
        self.rainha_anim = math.sin(self.t * 1.5 + 1) * 3

        if self.piscar_t > 0:
            self.piscar_t -= 1
            self.piscar = (self.piscar_t % 4 < 2)
        else:
            self.piscar = False

        if self.shake > 0:
            self.shake -= 1
        if self.flash_t > 0:
            self.flash_t -= 1
        if self.rainha_raiva and self.shake == 0:
            self.rainha_raiva = False

        for p in particulas[:]:
            p.update()
            if p.vida <= 0:
                particulas.remove(p)

    def draw(self):
        ox = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        oy = random.randint(-self.shake, self.shake) if self.shake > 0 else 0

        desenhar_fundo(self.t)

        if self.flash_t > 0 and self.flash_cor is not None:
            fl = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            alpha = int(self.flash_t * 15)
            fl.fill((*self.flash_cor, alpha))
            tela.blit(fl, (0, 0))

        desenhar_alice(
            tela,
            self.alice_x + ox,
            290 + int(self.alice_anim) + oy,
            escala=1.05,
            piscando=self.piscar
        )
        desenhar_rainha(
            tela,
            self.rainha_x + ox,
            295 + int(self.rainha_anim) + oy,
            escala=1.05,
            raiva=self.rainha_raiva
        )

        for p in particulas:
            p.draw(tela)

        barra_hp(50, 30, 280, 22, self.hp_alice, COR["hp_alice"], "Alice")
        barra_hp(570, 30, 280, 22, self.hp_rainha, COR["hp_rainha"], "Rainha de Copas")

        painel = pygame.Surface((LARGURA - 80, 80), pygame.SRCALPHA)
        painel.fill((10, 5, 25, 180))
        tela.blit(painel, (40, ALTURA - 110))
        pygame.draw.rect(tela, COR["rainha_coroa"], (40, ALTURA - 110, LARGURA - 80, 80), 2, border_radius=6)

        txt = fonte_media.render(self.mensagem, True, COR["texto"])
        tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA - 100))
        if self.sub_msg:
            sub = fonte_pequena.render(self.sub_msg, True, (200, 180, 150))
            tela.blit(sub, (LARGURA // 2 - sub.get_width() // 2, ALTURA - 72))

        if self.estado == "jogando":
            hint = fonte_pequena.render("[ESPAÇO] Atacar", True, (160, 220, 255))
        else:
            hint = fonte_pequena.render("[R] Recomeçar   [ESC] Sair", True, (200, 200, 200))
        tela.blit(hint, (LARGURA // 2 - hint.get_width() // 2, ALTURA - 40))

        titulo = fonte_grande.render("Alice vs Rainha de Copas", True, COR["amarelo"])
        sombra = fonte_grande.render("Alice vs Rainha de Copas", True, COR["preto"])
        tx = LARGURA // 2 - titulo.get_width() // 2
        tela.blit(sombra, (tx + 2, 422))
        tela.blit(titulo, (tx, 420))

        if self.estado in ("vitoria", "derrota"):
            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            tela.blit(overlay, (0, 0))
            cor_fim = COR["amarelo"] if self.estado == "vitoria" else (255, 80, 80)
            msg_fim = fonte_titulo.render(self.mensagem, True, cor_fim)
            tela.blit(msg_fim, (LARGURA // 2 - msg_fim.get_width() // 2, ALTURA // 2 - 40))

        pygame.display.flip()

#Loop Principal
def main():
    mostrar_introducao()
    jogo = Jogo()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if ev.key == pygame.K_SPACE:
                    jogo.atacar()
                if ev.key == pygame.K_r and jogo.estado != "jogando":
                    jogo.reiniciar()

        jogo.update()
        jogo.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()