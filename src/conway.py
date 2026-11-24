import taichi as ti
import time
import argparse

DIRECTIONS = [
  ti.math.ivec2(1, 1), ti.math.ivec2(1, 0), ti.math.ivec2(1, -1),
  ti.math.ivec2(0, 1), ti.math.ivec2(0, -1),
  ti.math.ivec2(-1, 1), ti.math.ivec2(-1, 0), ti.math.ivec2(-1, -1),
]

@ti.data_oriented
class Conway:
  def __init__(self, window_size: tuple, dims: tuple):
    self.window_size = window_size
    self.adj = ti.field(ti.i8, shape=dims)
    self.board = ti.field(ti.i8, shape=dims)
    self.img = ti.field(ti.f32, shape=window_size)

  def run(self):
    window = ti.ui.Window("Ising model", res=self.window_size)
    canvas = window.get_canvas()
    self._init_board()

    target_dt = 1.0 / 60.0
    dt = 0
    while window.running:
      t0 = time.perf_counter()
      if dt <= 1e-6:
        dt = target_dt
        self._simulate()

      self._render()
      canvas.set_image(self.img)
      window.show()

      ti.sync()
      dt -= time.perf_counter() - t0

  @ti.kernel
  def _init_board(self):
    for x, y in self.board: self.board[x, y] = 1 if ti.random(float) <= 0.5 else 0

  @ti.kernel
  def _simulate(self):
    for x, y in self.adj:
      self.adj[x, y] = 0
      for d in ti.static(DIRECTIONS): self.adj[x, y] += self.board[(ti.math.ivec2(x, y)+d)%self.board.shape]

    for x, y in self.board:
      if self.adj[x, y] == 3: self.board[x, y] = 1
      elif self.adj[x, y] != 2: self.board[x, y] = 0

  @ti.kernel
  def _render(self):
    for x, y in self.img:
      gx = (x * self.board.shape[0]) // self.window_size[0]
      gy = (y * self.board.shape[1]) // self.window_size[1]
      self.img[x, y] = self.board[gx, gy]

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="conway")
  parser.add_argument("--window_size", nargs=2, type=int, default=(1200, 1200))
  parser.add_argument("--dim", nargs=2, type=int, default=(120, 120))
  return parser

def main(argv: list[str] | None = None):
  parser = build_parser()
  args = parser.parse_args(argv)

  ti.init(arch=ti.cpu)
  print(args.window_size, args.dim)
  game = Conway(tuple(args.window_size), tuple(args.dim))
  game.run()

if __name__ == "__main__":
  main()
