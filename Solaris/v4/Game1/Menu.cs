using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using MainGame;
using Events;
using Cameras;


namespace Menus {

    public class Menu {

        MenuText[] menuText;
        MenuButton[] menuButtons;

        public Menu (MenuText[] menuText, MenuButton[] menuButtons) {
            this.menuText = menuText;
            this.menuButtons = menuButtons;
        }

        public void render(SpriteBatch spriteBatch) {
            // Render menu text items
            for (int i = 0; i < this.menuText.Length; i++) {
                this.menuText[i].render(spriteBatch);
            }
            // Render menu buttons
            for (int i = 0; i < this.menuButtons.Length; i++) {
                this.menuButtons[i].render(spriteBatch);
            }
        }

        public void update() {
            MouseState mouseState = Mouse.GetState();
            for (int i = 0; i < this.menuButtons.Length; i++) {
                this.menuButtons[i].update(mouseState);
            }
        }
    }

    public class MenuGenerator {

        SpriteFont[] fonts;

        public MenuGenerator(SpriteFont[] fonts) {
            this.fonts = fonts;
        }

        public Menu mainMenu(Camera camera) {
            // Make menu texts
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 200);
            MenuText titleSplash = new MenuText(this.fonts[4], "Solaris", titleSplashPos, Color.White);
            MenuText[] menuText = new MenuText[1];
            menuText[0] = titleSplash;
            // Make menu buttons
            MenuButton[] menuButtons = new MenuButton[3];
            // Play button
            Vector2 playButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 50);
            MenuButton playButton = new MenuButton(this.fonts[2], "Play", playButtonPos, Color.White, Color.Green, new ButtonEventArgs("play"));
            playButton.ButtonClicked += ButtonEvents.changeMenu;
            menuButtons[0] = playButton;
            // Settings button
            Vector2 settingButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2);
            MenuButton settingsButton = new MenuButton(this.fonts[2], "Settings", settingButtonPos, Color.White, Color.Green, new ButtonEventArgs("settings"));
            settingsButton.ButtonClicked += ButtonEvents.changeMenu;
            menuButtons[1] = settingsButton;
            // Quit button
            Vector2 quitButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 + 50);
            MenuButton quitButton = new MenuButton(this.fonts[2], "Quit", quitButtonPos, Color.White, Color.Red, new ButtonEventArgs("quit"));
            quitButton.ButtonClicked += ButtonEvents.changeMenu;
            menuButtons[2] = quitButton;
            // Make and return menu object
            Menu mainMenu = new Menu(menuText, menuButtons);
            return mainMenu;
        }

        public Menu pauseMenu(Camera camera) {
            // Make menu texts
            MenuText[] menuText = new MenuText[1];
            // Menu title
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 100);
            MenuText titleSplash = new MenuText(this.fonts[4], "Pause", titleSplashPos, Color.White);
            menuText[0] = titleSplash;
            // Make menu buttons
            MenuButton[] menuButtons = new MenuButton[2];
            // Play button
            Vector2 playButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 25);
            MenuButton playButton = new MenuButton(this.fonts[2], "Resume", playButtonPos, Color.White, Color.Green, new ButtonEventArgs("play"));
            playButton.ButtonClicked += Events.ButtonEvents.changeMenu;
            menuButtons[0] = playButton;
            // Main menu button
            Vector2 returnToMenuPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 + 25);
            MenuButton returnToMenuButton = new MenuButton(this.fonts[2], "Return to menu", returnToMenuPos, Color.White, Color.Green, new ButtonEventArgs("mainmenu"));
            returnToMenuButton.ButtonClicked += Events.ButtonEvents.changeMenu;
            menuButtons[1] = returnToMenuButton;
            // Make and return menu object
            Menu pauseMenu = new Menu(menuText, menuButtons);
            return pauseMenu;
        }

        public Menu settinsMenu(Camera camera) {
            // Make menu texts
            MenuText[] menuText = new MenuText[1];
            // Menu title
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 100);
            MenuText titleSplash = new MenuText(this.fonts[4], "Settings", titleSplashPos, Color.White);
            menuText[0] = titleSplash;
            // Make menu buttons
            MenuButton[] menuButtons = new MenuButton[2];
            // Placeholder button
            Vector2 placeholderButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2);
            MenuButton placeholderButton = new MenuButton(this.fonts[2], "Placeholder", placeholderButtonPos, Color.White, Color.Green, new ButtonEventArgs("mainmenu"));
            placeholderButton.ButtonClicked += Events.ButtonEvents.changeMenu;
            menuButtons[0] = placeholderButton;
            // Return to menu button
            Vector2 returnButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 + 50);
            MenuButton returnButton = new MenuButton(this.fonts[2], "Return to menu", returnButtonPos, Color.White, Color.Green, new ButtonEventArgs("mainmenu"));
            returnButton.ButtonClicked += Events.ButtonEvents.changeMenu;
            menuButtons[1] = returnButton;
            // Make and return menu object
            Menu pauseMenu = new Menu(menuText, menuButtons);
            return pauseMenu;
        }
    }

    public class MenuHandler {

        public Menu mainMenu;
        public Menu pauseMenu;
        public Menu settingsMenu;

        public Menu currentMenu;
        public bool displayMenu;

        public MenuHandler(SpriteFont[] fonts, Camera camera) {
            MenuGenerator menuGenerator = new MenuGenerator(fonts);
            this.mainMenu = menuGenerator.mainMenu(camera);
            this.pauseMenu = menuGenerator.pauseMenu(camera);
            this.settingsMenu = menuGenerator.settinsMenu(camera);

            this.currentMenu = this.mainMenu;
            this.displayMenu = true;
        }

        public void update() {
            currentMenu.update();
            return;
        }

        public bool render(SpriteBatch spriteBatch) {
            if (this.displayMenu == false) {
                return true;
            }
            currentMenu.render(spriteBatch);
            return false;
        }
    }
}
