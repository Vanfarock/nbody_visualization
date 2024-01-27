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

struct MainState {
    pos_x: Vec<f32>,
    circles: Vec<graphics::Mesh>,
}

impl MainState {
    fn new(circles: Vec<graphics::Mesh>) -> GameResult<MainState> {
        Ok(MainState {
            pos_x: vec![0., 200.],
            circles,
        })
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

        let mut i = 0;
        for circle in &self.circles {
            canvas.draw(circle, Vec2::new(self.pos_x[i], 380.0));
            i += 1;
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

    let circles = vec![
        make_circle(&ctx, vec2(0., 0.), 100.0, Color::WHITE)?,
        make_circle(&ctx, vec2(0., 0.), 100.0, Color::WHITE)?,
    ];
    let state = MainState::new(circles)?;
    event::run(ctx, event_loop, state)
}
