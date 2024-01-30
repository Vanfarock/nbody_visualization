use std::{
    error::Error,
    fs::{File, OpenOptions},
};

use ggez::{
    event,
    glam::*,
    graphics::{self, Color},
    Context, GameResult,
};
use nalgebra::Vector3;

#[derive(Clone, Copy)]
struct Body {
    pos: Vector3<f64>,
    vel: Vector3<f64>,
    mass: f64,
}

impl Body {
    fn new(pos: Vector3<f64>, vel: Vector3<f64>, mass: f64) -> Result<Body, ggez::GameError> {
        let body = Body { pos, vel, mass };

        Ok(body)
    }
}

struct GameObject {
    body: Body,
    mesh: graphics::Mesh,
}

impl GameObject {
    fn new(ctx: &Context, body: Body) -> Result<GameObject, ggez::GameError> {
        let game_object = GameObject {
            body,
            mesh: make_circle(ctx, &body.pos, 100., Color::WHITE)?,
        };

        Ok(game_object)
    }
}

struct MainState {
    game_objects: Vec<GameObject>,
}

impl MainState {
    fn new(game_objects: Vec<GameObject>) -> GameResult<MainState> {
        Ok(MainState { game_objects })
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

        for game_object in &self.game_objects {
            canvas.draw(&game_object.mesh, convert_to_point(&game_object.body.pos));
        }

        canvas.finish(ctx)?;

        Ok(())
    }
}

fn make_circle(
    ctx: &Context,
    position: &Vector3<f64>,
    radius: f32,
    color: Color,
) -> Result<graphics::Mesh, ggez::GameError> {
    graphics::Mesh::new_circle(
        ctx,
        graphics::DrawMode::fill(),
        convert_to_point(position),
        radius,
        2.0,
        color,
    )
}

fn convert_to_point(vector3: &Vector3<f64>) -> Vec2 {
    vec2(vector3.x as f32, vector3.y as f32)
}

fn open_file(filename: &str) -> Result<File, Box<dyn Error>> {
    let file = OpenOptions::new().write(true).append(true).open(filename)?;

    return Ok(file);
}

// fn parse_file(file: File) -> Result<Vec<GameObject>, Box<dyn Error>> {
//     Ok(())
// }

pub fn main() -> Result<(), Box<dyn Error>> {
    let cb = ggez::ContextBuilder::new("N-Body Visualization", "Vinícius Manuel Martins");
    let (ctx, event_loop) = cb.build()?;

    let file = open_file("test.json")?;

    let bodies: Vec<GameObject> = vec![
        GameObject::new(
            &ctx,
            Body::new(Vector3::new(0., 0., 0.), Vector3::new(0., 0., 0.), 100.)?,
        )?,
        GameObject::new(
            &ctx,
            Body::new(Vector3::new(100., 0., 0.), Vector3::new(0., 0., 0.), 100.)?,
        )?,
        GameObject::new(
            &ctx,
            Body::new(Vector3::new(0., 100., 0.), Vector3::new(0., 0., 0.), 100.)?,
        )?,
        GameObject::new(
            &ctx,
            Body::new(Vector3::new(100., 100., 0.), Vector3::new(0., 0., 0.), 100.)?,
        )?,
    ];
    let state = MainState::new(bodies)?;
    event::run(ctx, event_loop, state)
}
