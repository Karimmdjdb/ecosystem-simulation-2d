from utilities import *
from elements import Ground, Herb, Water, Cow, Mouse, Lion, Dragon, Camel, Rabbit
from planets import PlanetAlpha
import tkinter as tk
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MainWindow(tk.Tk):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.geometry(f"{MAIN_window_size[0]}x{MAIN_window_size[1]}")
        self.title("Simulion")

        self.background = tk.PhotoImage(file="resources/images/help.png")
        self.background = tk.PhotoImage(file="resources/images/main.png")
        can = tk.Canvas(self, width=MAIN_window_size[0], height=MAIN_window_size[1])
        can.create_image(MAIN_window_size[0]//2, MAIN_window_size[1]//2, image=self.background)
        can.pack()
        text1 = can.create_text(250, 150, anchor="nw", fill="white")
        can.itemconfig(text1, text="Welcome to the ecosystem simulator")
        text2 = can.create_text(295, 190, anchor="nw", fill="white")
        can.itemconfig(text2, text="Press start to begin !")
        tk.Button(self, text="Start", command=self.open_launch).place(x='280', y='240')
        tk.Button(self, text="Help", command=self.open_help).place(x='380', y='240')

    def open_help(self):
        HelpWindow().mainloop()

    def open_launch(self):
        self.destroy()
        LaunchWindow().mainloop()
class HelpWindow(tk.Toplevel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.geometry(f"350x450")
        self.title("Simulion - Help")
        self.iconphoto(False, tk.PhotoImage(file=ICON_PATH))
        self.background = tk.PhotoImage(file="resources/images/help.png")
        self.can = tk.Canvas(self, width=350, height=500)
        self.can.create_image(350//2, 450//2, image=self.background)

        self.texts = ["Press the escape key on the keyboard to exit the simulation","Press the directional arrows on the keyboard\nto move the camera","Click with the left mouse button on an animal to select\nit and display its informations  \n(right click anywhere to deselect)", "Press ctrl to enable/disable fps display", "Press the space bar to activate the apocalypse mode", "At the end of the simulation you will be able to see a graph\nthat summarizes the progress of the world", "No animals were harmed during the creation of this\nprogram, almost"]
        self.images = ["help_escape","help_arrows", "help_mouse", "help_fps", "help_apocalypse", "help_graph", "help_love"]

        tk.Button(self, text="<", command=self.previous_tip).place(x='130', y='375')
        tk.Button(self, text=">", command=self.next_tip).place(x='210', y='375')


        self.tip_index = 0
        self.text = self.can.create_text(20, 25, anchor="nw", fill="white")
        self.text2 = self.can.create_text(160, 380, anchor="nw", fill="white")
        self.can.itemconfig(self.text, text=self.texts[0])
        self.can.itemconfig(self.text2, text="Tip n°1")
        self.photo = tk.PhotoImage(file=f"resources/images/{self.images[0]}.png")
        self.can.create_image(180, 225, image=self.photo)

        self.can.pack()

    def previous_tip(self):

        self.tip_index -= 1
        if self.tip_index < 0:
            self.tip_index = 0

        self.can.itemconfig(self.text, text=self.texts[self.tip_index])
        self.can.itemconfig(self.text2, text=f"Tip n°{self.tip_index + 1}")
        self.photo = tk.PhotoImage(file=f"resources/images/{self.images[self.tip_index]}.png")
        self.can.create_image(180, 225, image=self.photo)

    def next_tip(self):

        self.tip_index += 1
        if self.tip_index > len(self.texts)-1:
            self.tip_index = len(self.texts)-1

        self.can.itemconfig(self.text, text=self.texts[self.tip_index])
        self.can.itemconfig(self.text2, text=f"Tip n°{self.tip_index + 1}")
        self.photo = tk.PhotoImage(file=f"resources/images/{self.images[self.tip_index]}.png")
        self.can.create_image(180, 225, image=self.photo)
class LaunchWindow(tk.Tk):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.geometry("700x400")
        self.title("Simulion")
        self.iconphoto(False, tk.PhotoImage(file=ICON_PATH))
        self.background = tk.PhotoImage(file="resources/images/help.png")
        can = tk.Canvas(self, width=MAIN_window_size[0], height=MAIN_window_size[1])
        can.create_image(MAIN_window_size[0]//2, MAIN_window_size[1]//2, image=self.background)
        can.pack()
        self.full_screen = tk.BooleanVar()
        tk.Checkbutton(self, text="FULL SCREEN", variable=self.full_screen, onvalue=1, offvalue=0).place(x='315', y='300')
        tk.Button(self, text="START", command=self.open_simulation).place(x='300', y='330')
        tk.Button(self, text="RETURN", command=self.return_main).place(x='370', y='330')
        animals = ["Dragon", "Lion", "Cow", "Camel", "Mouse", "Rabbit"]
        self.entries = {}
        for index,animal in enumerate(animals):
            x = 20 + index // 5 * 350
            y = 20 + index % 5 * 30
            text1 = can.create_text(x, y, anchor="nw", fill="white")
            can.itemconfig(text1, text=f"Number of {animal}s : ")
            self.entries[animal] = tk.Entry(self)
            self.entries[animal].insert(0, "0")
            self.entries[animal].place(x=f'{x+150}', y=f'{y}')


    def open_simulation(self):
        fs = self.full_screen.get()
        resolution = (self.winfo_screenwidth(), self.winfo_screenheight())
        animals_counts = {}
        all_good = True
        for key,value in self.entries.items():
            if value.get().isdecimal():
                animals_counts[key] = int(value.get())
            else:
                all_good = False
        if all_good:
            self.destroy()
            results = SimulationWindow().run(fs, resolution, animals_counts)
            ConfirmationWindow(results).mainloop()
        else:
            error_window = tk.Toplevel()
            error_window.geometry("200x100")
            tk.Label(error_window, text="Only integers allowed !").pack()
            error_window.mainloop()

    def return_main(self):
        self.destroy()
        MainWindow().mainloop()
class ConfirmationWindow(tk.Tk):
    def __init__(self, results, *args, **kw):
        super().__init__(*args, **kw)
        self.geometry(f"300x150")
        self.title("Simulion - Results")
        self.iconphoto(False, tk.PhotoImage(file=ICON_PATH))
        self.results = results
        self.background = tk.PhotoImage(file="resources/images/help.png")
        can = tk.Canvas(self, width=MAIN_window_size[0], height=MAIN_window_size[1])
        can.create_image(MAIN_window_size[0]//2, MAIN_window_size[1]//2, image=self.background)

        tk.Button(self, text="Yes", command=self.show_results).place(x='100', y='80')
        tk.Button(self, text="No", command=self.close).place(x='180', y='80')


        text = can.create_text(20, 30, anchor="nw", fill="white")
        can.itemconfig(text, text="Do you want to see the results of the simulation?")

        can.pack()

    def show_results(self):
        self.destroy()
        ResultsWindow(self.results).mainloop()

    def close(self):
        self.destroy()
class ResultsWindow(tk.Tk):
    def __init__(self, results, *args, **kw):
        super().__init__(*args, **kw)
        self.geometry(f"500x500")
        self.title("Simulion - Results")
        self.iconphoto(False, tk.PhotoImage(file=ICON_PATH))
        self.background = tk.PhotoImage(file="resources/images/help.png")
        can = tk.Canvas(self, width=500, height=1000)
        can.create_image(500//2, 500//2, image=self.background)
        can.pack()
        text1 = can.create_text(50, 25, anchor="nw", fill="white")
        can.itemconfig(text1, text="Here are the results of the simulation:\n(each graph represents the number of animals of the species at the moment)")
        years = len(results[list(results.keys())[0]])
        fig = Figure(figsize=(4, 4))
        a = fig.add_subplot(111)
        for animal, result in results.items():
            draw = False
            for value in result:
                if value != 0: draw = True
            if draw:
                a.plot(range(years), result, label=f"{animal}s")
        a.grid()
        a.set_ylabel("Number", fontsize=10)
        a.set_xlabel("Year", fontsize=10)
        a.legend()

        can2 = FigureCanvasTkAgg(fig, master=self)
        can2.get_tk_widget().place(x='50', y='75')
        can2.draw()

class SimulationWindow():
    def __init__(self):
        pass

    def run(self, is_full_screen, resolution, animals_counts):

        # Initialisations
        pygame.init()
        clock = pygame.time.Clock()
        vw = resolution[0] if is_full_screen else width
        vh = resolution[1] if is_full_screen else height
        camera = Camera(vw, vh)
        year_clock = Timer(10)
        cata_clock = Timer(2)
        red_sky = pygame.Surface((vw, vh), pygame.SRCALPHA)
        red_sky.fill((255, 0, 0, 60))
        key_verif_timer = CooldownTimer(0.5)
        apocalypse_logo = pygame.image.load(GUI_ICONS_PATH + "apocalypse.png")

        # GUI
        font = pygame.font.SysFont("Arial", 15)  # Police des texts
        color = (0, 0, 0)  # Couleur noire
        genders = [pygame.image.load(GUI_ICONS_PATH + "gender0.png"), pygame.image.load(GUI_ICONS_PATH + "gender1.png")]
        heart = pygame.image.load(GUI_ICONS_PATH + "heart.png")

        # Fênetre
        pygame.display.set_caption('Simulion')
        pygame.display.set_icon(pygame.image.load(GUI_ICONS_PATH + "window_icon.png"))
        screen = pygame.display.set_mode() if is_full_screen else pygame.display.set_mode(WINDOW_size)
        arrows_positions = [(vw/2 - CELL_SIZE/2, 5), (5, vh/2 - CELL_SIZE/2), (vw - CELL_SIZE - 5, vh/2 - CELL_SIZE/2), (vw/2 - CELL_SIZE/2, vh-CELL_SIZE - 5)]

        # Variables
        selected = None
        infos = ["", "", 0, (0, 0)]
        planet_age = 0
        results = {}
        for animal, number in animals_counts.items():
            results[animal] = [number]
        running = True
        apocalypse_mode = False
        show_fps = False
        selected_is_alive = False

        planet = PlanetAlpha('Terre', PLANET_LONGITUDE_CELLS_COUNT, PLANET_LATITUDE_CELLS_COUNT, Ground)

        # Placement des Elements
        planet.place_resources([Herb() for _ in range(HERBS_COUNT)])
        #planet.place_resources([Water() for _ in range(WATERS_COUNT)])
        for animal,count in animals_counts.items():
            planet.place_animals([globals()[animal]() for _ in range(count)])

        # Map
        map = [pygame.image.load(MAP_PATH + "map1.png"), pygame.image.load(MAP_PATH + "map2.png")]


        while running:

            #Enregistrement des resultats chaque année / ajout de ressources:
            if year_clock.is_up():
                planet_age += 1
                for val in results.values():
                    val.append(0)
                for animal in planet.get_animals():
                    results[animal.get_name()][planet_age] += 1
                herbs = 0
                for ressource in planet.get_resources():
                    if type(ressource) == Herb:
                        herbs += 1
                new_herbs = HERBS_COUNT - herbs
                planet.place_resources([Herb() for _ in range(new_herbs)])

            # Recupération des entrées
            mouse_x, mouse_y = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            # Mouvement de la camera
            camera_arrows_direction = [0, 0, 0, 0]
            if keys[pygame.K_UP]:
                camera.move(0, -10)
                camera_arrows_direction[0] = 1
            if keys[pygame.K_LEFT]:
                camera.move(-10, 0)
                camera_arrows_direction[1] = 1
            if keys[pygame.K_RIGHT]:
                camera.move(10, 0)
                camera_arrows_direction[2] = 1
            if keys[pygame.K_DOWN]:
                camera.move(0, 10)
                camera_arrows_direction[3] = 1
                
            # Activation du mode apocalypse
            if keys[pygame.K_SPACE]:
                apocalypse_mode = True

            # Activation/Desactivation de l'affichage des FPS
            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and key_verif_timer.is_up():
                show_fps = True if show_fps == False else False
                key_verif_timer.reset()

            # Verification de d'arrêt
            if keys[pygame.K_ESCAPE]:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False

            # Désélection de l'animal
            if pygame.mouse.get_pressed()[2] or not selected_is_alive:
                selected = None

            screen.fill(color)
            
            #affichage du ground layer de la map
            screen.blit(map[0], (-camera.offset()[0], -camera.offset()[1]))

            selected_is_alive = False

            for resource in planet.get_resources():
                if type(resource) == Herb:
                    resource.update(screen, camera)

            for animal in sorted(planet.get_animals(), key=lambda animal: animal.get_cord()[1]):
                if animal.get_id() == selected:
                    selected_is_alive = True
                    infos = [f"{animal.get_name()} {animal.get_age()}",f"[{animal.get_life()}/{animal.get_life_max()}]", animal.get_gender(), animal.get_cord()]

                animal.update(screen, camera)

                if year_clock.is_up():
                    animal.ageing()

                if apocalypse_mode and cata_clock.is_up():
                    animal.losing_life(random.randint(0, 2))

                # Sélection de l'animal
                if mouse_x <= animal.get_cord()[0] + CELL_SIZE - camera.offset()[0] and mouse_x >= animal.get_cord()[0] - camera.offset()[0] and mouse_y <= animal.get_cord()[1] + CELL_SIZE - camera.offset()[1] and mouse_y >= animal.get_cord()[1] - camera.offset()[1] and pygame.mouse.get_pressed()[0]:
                    selected = animal.get_id()
                    selected_is_alive = True

            if apocalypse_mode and cata_clock.is_up():
                for _ in range(50):
                    FireGFX((random.randint(0,MAP_size[0]), random.randint(0, MAP_size[1])))

            # Affichage des GFX
            GFX.draw_all(screen, camera)

            # Affichage du overlayer de la map
            screen.blit(map[1], (-camera.offset()[0], -camera.offset()[1]))

            # Affichage des infos de l'animal selectionné
            if selected != None:
                screen.blit(genders[infos[2]],(infos[3][0] - 35 - camera.offset()[0], infos[3][1] - 46 - camera.offset()[1]))
                screen.blit(heart, (infos[3][0] - 35 - camera.offset()[0], infos[3][1] - 28 - camera.offset()[1]))
                screen.blit(font.render(infos[0], True, color),(infos[3][0] - camera.offset()[0], infos[3][1] - 30 - camera.offset()[1]))
                screen.blit(font.render(infos[1], True, color),(infos[3][0] - camera.offset()[0], infos[3][1] - 15 - camera.offset()[1]))

            # Affichage du Mode apocalypse
            if apocalypse_mode:
                screen.blit(red_sky, (0, 0))
                screen.blit(apocalypse_logo, (vw - CELL_SIZE - 5, 5))
                screen.blit(font.render(f"APOCALYPSE MODE", True, color), (vw // 2 - 60, 30))

            # Affichage des fléches directionelles
            for arrow, position in zip(camera.cursor(camera_arrows_direction), arrows_positions):
                screen.blit(arrow, position)

            # Affichage des données textuelles
            screen.blit(font.render(f"World age : {planet_age} years", True, color), (5, 5))
            screen.blit(font.render(f"Animals count : {planet.get_current_animals_count()}", True, color), (5, 25))
            screen.blit(font.render(Messages.last_messages()[0], True, color), (5, vh-50))
            screen.blit(font.render(Messages.last_messages()[1], True, color), (5, vh-35))
            screen.blit(font.render(Messages.last_messages()[2], True, color), (5, vh-20))
            if show_fps:
                screen.blit(font.render(f"FPS : {round(clock.get_fps())}", True, color), (5, 45))

            pygame.display.flip()
            Timer.increase_all_timers()
            clock.tick(FPS)

        pygame.quit()
        return results