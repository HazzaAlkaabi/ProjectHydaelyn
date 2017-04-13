using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using MainGame;
using MenuEvents;


namespace Menus {
    public class MenuButton {

        public SpriteFont font;
        public string label;
        public Vector2 pos;
        public Vector2 centerPos;
        Vector2 size;
        public Color inactiveColor;
        public Color activeColor;
        private bool active = false;
        ButtonEventArgs args;
        ButtonState prevMouseButton;

        public event ButtonEventHandler ButtonClicked;

        public MenuButton(SpriteFont font, string label, Vector2 pos, Color inactiveColor, Color activeColor, ButtonEventArgs args) {
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

            prevMouseButton = ButtonState.Released;
        }

        public void update(MouseState mouseState) {
            Vector2 mousePos = new Vector2(mouseState.X, mouseState.Y);
            this.active = false;
            bool xActive = false;
            bool yActive = false;
            if (mousePos.X >= this.pos.X - (this.size.X / 2) && mousePos.X <= this.pos.X + (this.size.X / 2)) {
                xActive = true;
            }
            if (xActive == true && mousePos.Y >= this.pos.Y - (this.size.Y / 2) && mousePos.Y <= this.pos.Y + (this.size.Y / 2)) {
                yActive = true;
            }
            // The mouse is within the confines of the button
            if (xActive == true && yActive == true) {
                this.active = true;
            }

            if (this.active == true && mouseState.LeftButton == ButtonState.Released && this.prevMouseButton == ButtonState.Pressed) {
                // raise the event for the event handler
                if (ButtonClicked != null) {
                    ButtonClicked(this, this.args);
                }
            }

            this.prevMouseButton = mouseState.LeftButton;
        }

        public void render(SpriteBatch spriteBatch) {
            Color color = this.inactiveColor;
            if (this.active == true) {
                color = this.activeColor;
            }
            spriteBatch.DrawString(this.font, this.label, this.centerPos, color);
        }
    }
}
