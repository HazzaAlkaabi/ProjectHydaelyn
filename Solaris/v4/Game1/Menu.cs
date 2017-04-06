using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Game1;


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

    public class MenuButton {

        public SpriteFont font;
        public string label;
        public Vector2 pos;
        public Vector2 centerPos;
        Vector2 size;
        public Color inactiveColor;
        public Color activeColor;
        private bool active = false;
        EventArgs args;

        public event EventHandler ButtonClicked;

        public MenuButton(SpriteFont font, string label, Vector2 pos, Color inactiveColor, Color activeColor, EventArgs args) {
            this.font = font;
            this.label = label;
            // Find dimensions of the text adn set position to be the center of the text
            Vector2 size = font.MeasureString(label);
            Vector2 centerPos = new Vector2(pos.X - size.X / 2, pos.Y - size.Y / 2);
            this.centerPos = centerPos;
            this.pos = pos;
            this.size = size;
            this.inactiveColor = inactiveColor;
            this.activeColor = activeColor;
            this.args = args;
        }

        public void update(MouseState mouseState) {
            Vector2 mousePos = new Vector2(mouseState.X, mouseState.Y);
            this.active = false;
            bool xActive = false;
            bool yActive = false;
            if (mousePos.X >= this.pos.X - (this.size.X / 2) && mousePos.X <= this.pos.X + (this.size.X / 2)) {
                xActive = true;
            }
            if (xActive == true && mousePos.Y >= this.pos.Y - (this.size.Y /2 ) && mousePos.Y <= this.pos.Y + (this.size.Y / 2)) {
                yActive = true;
            }
            // The mouse is within the confines of the button
            if (xActive == true && yActive == true) {
                this.active = true;
            }

            if (this.active == true && mouseState.LeftButton == ButtonState.Pressed) {
                // raise the event for the event handler
                if (ButtonClicked != null) {
                    ButtonClicked(this, this.args);
                }
                
            }
        }

        public void render(SpriteBatch spriteBatch) {
            Color color = this.inactiveColor;
            if (this.active == true) {
                color = this.activeColor;
            }
            spriteBatch.DrawString(this.font, this.label, this.centerPos, color);
        }
    }

    public class MenuText {

        public SpriteFont font;
        public string text;
        public Vector2 pos;
        public Color color;

        public MenuText(SpriteFont font, string text, Vector2 pos, Color color) {
            // Find the center point of the text and set the new position so the text is rendered centered on the given position
            this.font = font;
            this.text = text;
            Vector2 size = font.MeasureString(text);
            Vector2 centerPos = new Vector2(pos.X - size.X / 2, pos.Y - size.Y / 2);
            this.pos = centerPos;
            this.color = color;
        }

        public void render(SpriteBatch spriteBatch) {
            // Render the given text
            spriteBatch.DrawString(this.font, this.text, this.pos, this.color);
        }
    }

    public class MenuGenerator {

        SpriteFont[] fonts;

        public MenuGenerator(SpriteFont[] fonts) {
            this.fonts = fonts;
        }

        public Menu mainMenu(Camera camera) {
            // Make menu texts
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 100);
            MenuText titleSplash = new MenuText(this.fonts[4], "Solaris", titleSplashPos, Color.White);
            MenuText[] menuText = new MenuText[1];
            menuText[0] = titleSplash;
            // Make menu buttons
            Vector2 playButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2);
            MenuButton playButton = new MenuButton(this.fonts[2], "Play", playButtonPos, Color.White, Color.Green, EventArgs.Empty);
            playButton.ButtonClicked += Events.EventHandler.changeMenu;
            MenuButton[] menuButtons = new MenuButton[1];
            menuButtons[0] = playButton;
            Menu mainMenu = new Menu(menuText, menuButtons);
            return mainMenu;
        }

        public Menu pauseMenu(Camera camera) {
            // Make menu texts
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 100);
            MenuText titleSplash = new MenuText(this.fonts[4], "Pause", titleSplashPos, Color.White);
            MenuText[] menuText = new MenuText[1];
            menuText[0] = titleSplash;
            // Make menu buttons
            Vector2 playButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2);
            MenuButton playButton = new MenuButton(this.fonts[2], "Resume", playButtonPos, Color.White, Color.Green, EventArgs.Empty);
            MenuButton[] menuButtons = new MenuButton[1];
            menuButtons[0] = playButton;
            Menu pauseMenu = new Menu(menuText, menuButtons);
            return pauseMenu;
        }

        public Menu settinsMenu(Camera camera) {
            // Make menu texts
            Vector2 titleSplashPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2 - 100);
            MenuText titleSplash = new MenuText(this.fonts[4], "Settings", titleSplashPos, Color.White);
            MenuText[] menuText = new MenuText[1];
            menuText[0] = titleSplash;
            // Make menu buttons
            Vector2 playButtonPos = new Vector2(camera.resolution.X / 2, camera.resolution.Y / 2);
            MenuButton settingsButton = new MenuButton(this.fonts[2], "Change some settings", playButtonPos, Color.White, Color.Green, EventArgs.Empty);
            MenuButton[] menuButtons = new MenuButton[1];
            menuButtons[0] = settingsButton;
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

        public bool update() {
            if (this.displayMenu == false) {
                return true;
            }
            currentMenu.update();
            return false;
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
