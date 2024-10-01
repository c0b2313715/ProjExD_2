import os
import sys
import random
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(+5,0),}
KK ={(0,-5):0,
     (+5,-5):1,
     (+5,0):2,
    (+5,+5):3,
    (0,+5):4,
    (-5,+5):5,
    (-5,0):6,
    (-5,-5):7,
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def game_over(screen):
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    si_img=pg.image.load("fig/8.png")  # 泣いているこかとん
    si_rct=si_img.get_rect()
    go_img=pg.Surface((WIDTH,HEIGHT))  # ブラックスクリーン
    pg.draw.rect(go_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    go_img.set_alpha(10)
    fonto =pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255,255,255))
    screen.blit(go_img,[0,0])
    screen.blit(txt,(WIDTH/2-150,HEIGHT/2-50))
    screen.blit(si_img,[WIDTH//2-200,HEIGHT//2-50])
    screen.blit(si_img,[WIDTH//2+170,HEIGHT//2-50])
    pg.display.update()
    pg.display.update()
       
def kk_imges(m):
    list=[i for i in range(0,360,45)]
    mk=()
    for j in range(len(list)):
        kk_img = pg.transform.rotozoom(pg.image.load(m), list[j], 0.9)
        kk_rct = kk_img.get_rect()
        mk+=(kk_img,kk_rct)
    return mk



def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん、または、爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate =True,True
    if obj_rct.left <0 or WIDTH < obj_rct.right :
        yoko = False
    if obj_rct.top <0 or HEIGHT < obj_rct.bottom :
        tate = False
    return yoko,tate

def bb_accs(n)-> int:
    accs = [a for a in range(1, 11)]
    a=accs[n[1]]
    b=a+int(n[2])
    return b

# def bb_imgs(n):
#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
#       #  if r is None n[1]:
#         return bb_img



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    kk=kk_imges("fig/3.png")  # こうかとん画像
    bb_img = pg.Surface((20,20))
    bb_img .set_colorkey((0,0,0))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
#    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy= +5,+5
    si_img=pg.image.load("fig/8.png")  # 泣いているこかとん
    go_img=pg.Surface((WIDTH,HEIGHT))  # ブラックスクリーン
    pg.draw.rect(go_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    go_img.set_alpha(100)
    fonto =pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255,255,255))
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら。（逆でもおなじみになる）
            screen.blit(go_img,[0,0])
            screen.blit(txt,(WIDTH/2-150,HEIGHT/2-50))
            screen.blit(si_img,[WIDTH//2-200,HEIGHT//2-50])
            screen.blit(si_img,[WIDTH//2+170,HEIGHT//2-50])
            pg.display.update()
            time.sleep(5)
            return 
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        # for r in range(1, 11):
        #     bb_img = pg.Surface((20*r, 20*r))
        #     pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        for key,tup in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tup[0]  # 横方向
                sum_mv[1] += tup[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        # for key,tyo in KK.items():
        #     if sum_mv[key]:
        #         kk_rct=kk[tyo]
        # screen.blit(kk_img, kk_rct)
        bb_rct.move_ip((vx,vy))
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy *=-1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        # avx = vx*bb_accs[min(tmr//500, 9)]
        # vx,vy=avx,avx
        # bb_img = bb_imgs[min(tmr//500, 9)]
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
