using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Game1;

namespace Bodies {

    class Body {

        Vector2 pos;
        float size;
        Color color;

        public Body(Vector2 pos, float size, Color color) {
            this.pos = pos;
            this.size = size;
            this.color = color;
        }

        public void update() {
            // TODO: orbit mechanics?
        }

        public void render(SpriteBatch spriteBatch, Camera camera) {
            // TODO: render shape to screen
        }
    }

    class Player {

        Vector2 pos;
        Vector2 vel;
        float size;
        Color color;


        public Player(Vector2 pos, float size, Color color) {
            this.pos = pos;
            this.size = size;
            this.color = color;
            this.vel = new Vector2(0, 0);
        }

        public void update() {
            // TODO: gravity or something? apply velocity to pos
        }

        public void render(SpriteBatch spriteBatch, Camera camera) {
            // TODO: draw player to screen
        }
    }
}
