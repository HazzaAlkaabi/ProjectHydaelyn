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

namespace Menus {
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
}
