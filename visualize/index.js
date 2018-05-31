function draw() {
  draw_canvas(document.getElementById('graph_1_1'), "log/a_1_r_1_theta_0.0564.json")
  draw_canvas(document.getElementById('graph_1_2'), "log/a_1_r_2_theta_0.1129.json")
  draw_canvas(document.getElementById('graph_1_3'), "log/a_1_r_3_theta_0.1698.json")
  draw_canvas(document.getElementById('graph_2_1'), "log/a_2_r_1_theta_0.0564.json")
  draw_canvas(document.getElementById('graph_2_2'), "log/a_2_r_2_theta_0.1129.json")
  draw_canvas(document.getElementById('graph_2_3'), "log/a_2_r_3_theta_0.1698.json")
  draw_canvas(document.getElementById('graph_3_1'), "log/a_3_r_1_theta_0.0564.json")
  draw_canvas(document.getElementById('graph_3_2'), "log/a_3_r_2_theta_0.1129.json")
  draw_canvas(document.getElementById('graph_3_3'), "log/a_3_r_3_theta_0.1698.json")
}

function draw_canvas(canvas, logfile) {
  if (canvas.getContext) {
    let ctx = canvas.getContext("2d")
    let data = []
    $.getJSON(logfile, (d) => { data = d })
    let index = 0
    setInterval(() => {
      if (data[index]) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        draw_stick(ctx, data[index]["theta"])
        draw_ball(ctx, data[index]["r"] * 100, data[index]["theta"])
        index = index + 1
      } else {
        index = 0
      }
    }, 20)
  }
}

function ball_y(r, R, theta) {
  return 450 - (r - Math.tan(theta) * R) * Math.sin(theta) - R / Math.cos(theta)
}

function ball_x(r, R, theta) {
  return 450 + (r - Math.tan(theta) * R) * Math.cos(theta)
}

function draw_stick(ctx, theta) {
  ctx.moveTo(450 + 400 * Math.cos(theta), 450 - 400 * Math.sin(theta))
  ctx.lineTo(450 - 400 * Math.cos(theta), 450 + 400 * Math.sin(theta))
  ctx.stroke()
}

function draw_ball(ctx, r, theta) {
  ctx.beginPath()
  ctx.arc(ball_x(r, 30, theta), ball_y(r, 30, theta), 30, 0, 2 * Math.PI)
  ctx.stroke()
}

function clean_all() {

  }
