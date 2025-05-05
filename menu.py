import sys
import gui
import pygame
import ResourceManager

class MainMenu:
    def __init__(self,window:pygame.Window):
        self.run_splash = True
        self.window = window
        window.get_surface()
        self.splash_screens:list[tuple[pygame.Surface,int,int,int]] = [
            (pygame.image.load('./Images/MainMenu/pygame_ce_powered.png').convert_alpha(),500,800,1000),
        ]

        bg_image = pygame.image.load('./Images/MainMenu/Background.png').convert()
        bg_image = pygame.transform.scale(bg_image,window.size)

        cs = gui.ColorScheme(100,100,100)
        self.layer = gui.Layer(window.size)
        self.layer.space.addObjects(
            gui.ui.Image((-0,-0),bg_image),
            gui.ui.positioners.Aligner(
                gui.ui.Image((0,0),pygame.Surface(((0,0)))),
                0.5,0.2
            ),
            gui.ui.WithAlpha(
                gui.ui.positioners.Aligner(
                    gui.ui.AddText(
                        gui.ui.Button((0,-25),(100,50),cs,None,self.toGame),
                        'Play','white',pygame.font.SysFont('Arial',20)
                    ),
                    0.5,0.5
                ),
                alpha=200
            ),
            # gui.ui.WithAlpha(
            #     gui.ui.positioners.Aligner(
            #         gui.ui.AddText(
            #             gui.ui.Button((0,55-25),(100,50),cs,None,self.goToSettings),
            #             'Settings','white',pygame.font.SysFont('Arial',20)
            #         ),
            #         0.5,0.5
            #     ),
            # alpha=200
            # ),
            gui.ui.WithAlpha(
                gui.ui.positioners.Aligner(
                    gui.ui.AddText(
                        gui.ui.Button((0,2*55-25),(100,50),cs,self.quit),
                        'Quit','white',pygame.font.SysFont('Arial',20)
                    ),
                    0.5,0.5
                ),
            alpha=200
            )
        )

    def goToMain(self):
        self.cur_layer = self.layer

    def toGame(self):
        self.running = False
    
    def quit(self):
        sys.exit()

    def runSplashScreensAsync(self):
        if not self.splash_screens:return
        screen = self.window.get_surface()
        i = 0
        splash_img,fade_in,stay,fade_out = self.splash_screens[i]
        state = 'fade_in'
        time = pygame.time.get_ticks()
        while True:
            screen.fill('black')
            t_cur = pygame.time.get_ticks()
            if state == 'fade_in':
                p = (t_cur - time) / fade_in
                splash_img.set_alpha(min(255,int(p * 255)))
                screen.blit(splash_img,((screen.get_width()-splash_img.get_width())//2,(screen.get_height()-splash_img.get_height())//2))
                if p >= 1:
                    time += fade_in
                    splash_img.set_alpha(255)
                    state = 'stay'
            if state == 'stay':
                if t_cur >= time + stay:
                    state = 'fade_out'
                    time += stay
                screen.blit(splash_img,((screen.get_width()-splash_img.get_width())//2,(screen.get_height()-splash_img.get_height())//2))
            if state == 'fade_out':
                p = (t_cur - time) / fade_in
                # s = f'{p} -> {max(0,int((1-p) * 255))}'
                # screen.blit(pygame.font.SysFont(None,20).render(s,True,'white'))
                splash_img.set_alpha(max(0,int((1-p) * 255)))
                screen.blit(splash_img,((screen.get_width()-splash_img.get_width())//2,(screen.get_height()-splash_img.get_height())//2))
                if p >= 1:
                    time += fade_out
                    splash_img.set_alpha(0)
                    i += 1
                    if i == len(self.splash_screens):
                        break
                    splash_img,fade_in,stay,fade_out = self.splash_screens[i]
                    state = 'fade_in'
            yield       

    def runSplashScreens(self):
        for _ in self.runSplashScreensAsync():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return
            self.window.flip()

    def run(self):
        if self.run_splash:
            self.runSplashScreens()
            self.run_splash = False
        self.running = True
        self.cur_layer = self.layer
        screen = self.window.get_surface()
        clock = pygame.time.Clock()
        while self.running:
            inp = gui.utils.getInput()
            if inp.quitEvent or inp.consumeKey(pygame.K_ESCAPE):
                sys.exit()
            self.cur_layer.update(inp)
            self.cur_layer.draw(screen)
            self.window.flip()
            dt = clock.tick(60) 
            self.dt  = dt / 1000

if __name__ == '__main__':
    print('!!Debug Only!!')
    pygame.init()
    win = pygame.Window('menu test',(1920,1080),fullscreen=True)
    menu = MainMenu(win)
    menu.run()

