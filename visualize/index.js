function draw() {
  let canvas = document.getElementById('graph')
  if (canvas.getContext) {
    let ctx = canvas.getContext("2d")
    let data = []
    $.getJSON("log.json", (d) => { data = d })
    let index = 0
    setInterval(() => {
      if (data[index]) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        draw_stick(ctx, data[index]["theta"])
        draw_ball(ctx, data[index]["r"] * 100, data[index]["theta"])
        index = index + 1
      }
    }, 20)
  }
}

function ball_y(r, R, theta) {
  return 250 - (r - Math.tan(theta) * R) * Math.sin(theta) - R / Math.cos(theta)
}

function ball_x(r, R, theta) {
  return 250 + (r - Math.tan(theta) * R) * Math.cos(theta)
}

function draw_stick(ctx, theta) {
  ctx.moveTo(250 + 200 * Math.cos(theta), 250 - 200 * Math.sin(theta))
  ctx.lineTo(250 - 200 * Math.cos(theta), 250 + 200 * Math.sin(theta))
  ctx.stroke()
}

function draw_ball(ctx, r, theta) {
  ctx.beginPath()
  ctx.arc(ball_x(r, 10, theta), ball_y(r, 10, theta), 10, 0, 2 * Math.PI)
  ctx.stroke()
}

function clean_all() {

  }
