//! The simplest possible example that does something.
#![allow(clippy::unnecessary_wraps)]

use ggez::{
    event,
    glam::*,
    graphics::{self, Color},
    Context, GameResult,
};

struct Body {
    pos: Vec2,
    mass: f32,
    mesh: graphics::Mesh,
}

impl Body {
    fn new(ctx: &Context, pos: Vec2, mass: f32) -> Result<Body, ggez::GameError> {
        let body = Body {
            pos,
            mass,
            mesh: make_circle(ctx, pos, 100., Color::WHITE)?,
        };

        Ok(body)
    }
}

struct MainState {
    bodies: Vec<Body>,
}

impl MainState {
    fn new(bodies: Vec<Body>) -> GameResult<MainState> {
        Ok(MainState { bodies })
    }
}

impl event::EventHandler<ggez::GameError> for MainState {
    fn update(&mut self, _ctx: &mut Context) -> GameResult {
        // self.pos_x = self.pos_x % 800.0 + 1.0;
        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult {
        let mut canvas =
            graphics::Canvas::from_frame(ctx, graphics::Color::from([0.1, 0.2, 0.3, 1.0]));

        for body in &self.bodies {
            canvas.draw(&body.mesh, body.pos);
        }

        canvas.finish(ctx)?;

        Ok(())
    }
}

fn make_circle(
    ctx: &Context,
    position: Vec2,
    radius: f32,
    color: Color,
) -> Result<graphics::Mesh, ggez::GameError> {
    graphics::Mesh::new_circle(
        ctx,
        graphics::DrawMode::fill(),
        position,
        radius,
        2.0,
        color,
    )
}

pub fn main() -> GameResult {
    let cb = ggez::ContextBuilder::new("N-Body Visualization", "Vinícius Manuel Martins");
    let (ctx, event_loop) = cb.build()?;

    let bodies: Vec<Body> = vec![
        Body::new(&ctx, vec2(0., 0.), 100.)?,
        Body::new(&ctx, vec2(100., 0.), 100.)?,
        Body::new(&ctx, vec2(0., 100.), 100.)?,
        Body::new(&ctx, vec2(100., 100.), 100.)?,
    ];
    let state = MainState::new(bodies)?;
    event::run(ctx, event_loop, state)
}
