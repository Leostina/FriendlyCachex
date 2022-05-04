let stepCount = 0;
let playerRed = true;
let result = {
  steps:[],
  board:[]
};
let state = {};
let elems = {};
let canSteal = true;

function hexRange(n) {
  let a = [];
  for (let row = 0; row < n; row += 1) {
    for (let col = 0; col < n; col += 1) {
        a.push([row, col]);
    }
  }
  return a;
}

// // //
// UI Functions for drawing and manipulating SVG hex grid
//
function svgElement(tag = "svg", attrs = {}, style = {}) {
  let element = document.createElementNS("http://www.w3.org/2000/svg", tag);
  Object.entries(attrs).forEach(([key, val]) => {
    element.setAttributeNS(null, key, val.toString());
  });
  Object.entries(style).forEach(([key, val]) => {
    element.style[key] = val.toString();
  });
  return element;
}

function svgHex(r, q, size, style, radius=1) {
  let x = size * (1.73 * q + 0.866 * r);
  let y = size * (-1.5 * r);

  // build points string
  let points = [0, 1, 2, 3, 4, 5].map((i) => [
    x + radius * size * Math.sin((i * Math.PI) / 3),
    y + radius * size * Math.cos((i * Math.PI) / 3)
  ]);
  let pointsStr = points.map((xy) => xy.join(",")).join(" ");

  // build SVG element
  return svgElement(
    "polygon",
    { points: pointsStr },
    style,
  );
}

function svgCircle(x, y, r, style) {
  return svgElement("circle", { cx: x, cy: y, r: r }, style);
}

function svgText(x, y, s, style) {
  let text = svgElement(
    "text",
    {
      x: x,
      y: y,
      "dominant-baseline": "middle",
      "text-anchor": "middle"
    },
    style
  );
  text.innerHTML = s;
  return text;
}

function svgToken(r, q, size, isRed) {
  let x = size * (1.73 * q + 0.866 * r);
  let y = size * (-1.5 * r);
  // build SVG element
  let token = svgElement("g", {}, { "pointer-events": "none" });
  token.appendChild(
    svgCircle(x, y, size * 0.55, {
      fill: "transparent",
      stroke: playerRed ? "red":"blue",
      strokeWidth: "2.5px"
    })
  );
  
  playerRed = !playerRed;

  return token;
}

function steal() {
  
  let svg = document.getElementById("s");
  let out = document.getElementById("output");
  let dla = document.getElementById("download");
  result["steps"].push(["b", -1, -1]);
  piece = result["board"][0] 
  result["board"][0] = ["b", piece[2], piece[1]];
  
  
  svg.removeChild(elems[[piece[1], piece[2]]]);
  elems[[piece[2], piece[1]]] = svgToken(piece[2], piece[1], SIZE, false);
  svg.appendChild(elems[[piece[2], piece[1]]]);


  updateSource(out, dla);
}

function svgHexGrid(radius, onclick, size) {
  let grid = svgElement("g");
  hexRange(radius).forEach(([r, q]) => {
    let hex = svgHex(
      r,
      q,
      size, 
      {
        fill: "#dadada",
        stroke: "black",
        strokeWidth: "1px"
      }
    );
    hex.addEventListener(
      "click",
      e => {
        if (inBoard('r', r, q) || inBoard('b', r, q)) {
          
        }
        else{

        checkCapture(r, q);
        result["board"].push([playerRed?"r":"b",r,q]);
        result["steps"].push([playerRed?"r":"b",r,q]);
        
        
        
        nextColor.innerHTML = !playerRed ? "next player: RED" : "next player: BLUE"
        nextColor.style.color = !playerRed ? "red" : "blue"
        
        
        
          stepCount += 1;
          if (stepCount == 1) {
            document.getElementById("steal").innerHTML = "Your chance for STEALing this piece from your opponent is coming, the only chance in this game, catch it by pressing F"
            this.addEventListener("keyup", e => {
              if (e.key === 'f' & canSteal)
              {
                console.log("stealed");
                steal();
                nextColor.innerHTML = playerRed ? "next player: RED" : "next player: BLUE"
                nextColor.style.color = playerRed ? "red" : "blue"
                canSteal = false;
              }

            })
            
  

          }
          else
          {
            document.getElementById("steal").innerHTML = ""
          
          }


        onclick(e, r, q);
          return false; 
          }
      },
      false
    );
    grid.appendChild(hex);
    
  let nextColor = document.getElementById("nextColorLbl");

  });
  return grid;
}


// Control functions for setting the UI based on the state
//
function toToken(i) {
  return ["blank", ""];
}

function inBoard(c, q, r)
{
  if (result["board"].find(el=> (el[0] === c && el[1] === q && el[2] === r)))
    {
      return true;
    }
  return false;
}

function removePiece(c, q, r)
{
  result["board"] = result["board"].filter(el => !(el[0] === c && el[1] === q && el[2] === r));
}

function updateSource(out, link) {

  let source = JSON.stringify(result, null, 2);
  out.innerHTML = source;
  link.setAttribute(
    'href',
    'data:text/plain;charset=utf-8,' + encodeURIComponent(source)
  );
}
SIZE = 7
N = 15

function exeRemoval(r1, q1, r2, q2, c)
{
  removePiece(c, r1, q1);
  removePiece(c, r2, q2);
  document.getElementById("s").removeChild(elems[[r1, q1]]);
  document.getElementById("s").removeChild(elems[[r2, q2]]);
}

function checkCapture(r, q) {

  console.log((result["board"].includes(["r",r,q+1]))?"Yes":"No");
  console.log([r,q]);
  if (playerRed)
    {
      if (inBoard("r", r, q - 1) && inBoard("b", r + 1, q - 1) && inBoard("b", r - 1, q)) {
        exeRemoval(r + 1, q - 1, r - 1, q, 'b');
      }
  
      if (inBoard("r",r,q+1) && inBoard("b",r+1,q) && inBoard("b",r-1,q+1))
      {
        exeRemoval(r+1, q, r - 1, q+1, 'b');
    }
    
      if (inBoard("r",r+1,q-1) && inBoard("b",r,q-1) && inBoard("b",r+1,q))
      {
        exeRemoval(r, q-1,r+ 1, q, 'b');
    }
    
      if (inBoard("r",r-1,q+1) && inBoard("b",r-1,q) && inBoard("b",r,q+1))
      {
        exeRemoval(r-1, q,r, q+1, 'b');
    }
    
    
      if (inBoard("r",r-1,q) && inBoard("b",r,q-1) && inBoard("b",r-1,q+1))
      {
        exeRemoval(r, q-1,r-1, q+1, 'b');
    }
    
        if (inBoard("r",r+1,q) && inBoard("b",r+1,q-1) && inBoard("b",r,q+1))
      {
        exeRemoval(r+1, q-1,r, q+1, 'b');
      }

    
          // 1.5 dist
        if (inBoard("r",r+2,q-1) && inBoard("b",r+1,q-1) && inBoard("b",r+1,q))
      {
        exeRemoval(r+1, q-1,r+1, q, 'b');
    }
        if (inBoard("r",r-2,q+1) && inBoard("b",r-1,q) && inBoard("b",r-1,q+1))
      {
        exeRemoval(r-1, q,r-1, q+1, 'b');
    }
        if (inBoard("r",r+1,q-2) && inBoard("b",r,q-1) && inBoard("b",r+1,q-1))
      {
        exeRemoval(r, q-1,r+1, q-1, 'b');
    }
        if (inBoard("r",r-1,q+2) && inBoard("b",r-1,q+1) && inBoard("b",r,q+1))
      {
        exeRemoval(r-1, q+1,r, q+1, 'b');
    }
    
        if (inBoard("r",r-1,q-1) && inBoard("b",r,q-1) && inBoard("b",r-1,q))
      {
        exeRemoval(r, q-1,r-1, q, 'b');
    }
            if (inBoard("r",r+1,q+1) && inBoard("b",r+1,q) && inBoard("b",r,q+1))
      {
        exeRemoval(r+1, q,r, q+1, 'b');
    }
  }

  else {
    
      if (inBoard("b", r, q - 1) && inBoard("r", r + 1, q - 1) && inBoard("r", r - 1, q)) {
        exeRemoval(r + 1, q - 1, r - 1, q, 'r');
      }
  
      if (inBoard("b",r,q+1) && inBoard("r",r+1,q) && inBoard("r",r-1,q+1))
      {
        exeRemoval(r+1, q, r - 1, q+1, 'r');
    }
    
      if (inBoard("b",r+1,q-1) && inBoard("r",r,q-1) && inBoard("r",r+1,q))
      {
        exeRemoval(r, q-1,r+ 1, q, 'r');
    }
    
      if (inBoard("b",r-1,q+1) && inBoard("r",r-1,q) && inBoard("r",r,q+1))
      {
        exeRemoval(r-1, q,r, q+1, 'r');
    }
    
    
      if (inBoard("b",r-1,q) && inBoard("r",r,q-1) && inBoard("r",r-1,q+1))
      {
        exeRemoval(r, q-1,r-1, q+1, 'r');
    }
    
        if (inBoard("b",r+1,q) && inBoard("r",r+1,q-1) && inBoard("r",r,q+1))
      {
        exeRemoval(r+1, q-1,r, q+1, 'r');
    }
    
      // 1.5 dist
        if (inBoard("b",r+2,q-1) && inBoard("r",r+1,q-1) && inBoard("r",r+1,q))
      {
        exeRemoval(r+1, q-1,r+1, q, 'r');
    }
        if (inBoard("b",r-2,q+1) && inBoard("r",r-1,q) && inBoard("r",r-1,q+1))
      {
        exeRemoval(r-1, q,r-1, q+1, 'r');
    }
        if (inBoard("b",r+1,q-2) && inBoard("r",r,q-1) && inBoard("r",r+1,q-1))
      {
        exeRemoval(r, q-1,r+1, q-1, 'r');
    }
        if (inBoard("b",r-1,q+2) && inBoard("r",r-1,q+1) && inBoard("r",r,q+1))
      {
        exeRemoval(r-1, q+1,r, q+1, 'r');
    }
    
        if (inBoard("b",r-1,q-1) && inBoard("r",r,q-1) && inBoard("r",r-1,q))
      {
        exeRemoval(r, q-1,r-1, q, 'r');
    }
            if (inBoard("b",r+1,q+1) && inBoard("r",r+1,q) && inBoard("r",r,q+1))
      {
        exeRemoval(r+1, q,r, q+1, 'r');
    }
  }
}


function main() { 
  result = {
  steps:[],
  board:[]
  };
  canSteal = true;
  stepCount = 0;
  playerRed = true;
  N = document.querySelector('input').value;
  
  let redPlayer = true;
  
  let svg = document.getElementById("s");
  svg.innerHTML = ''; // resetF
  document.getElementById("nextColorLbl").innerHTML = 'next player: RED';
  document.getElementById("nextColorLbl").style.color = 'red';
  let out = document.getElementById("output");
  let dla = document.getElementById("download");
  let colorLbl = document.getElementById("colorLbl");
  let nextColor = document.getElementById("nextColorLbl");
  state = {};
  elems = {};
  hexRange(N).forEach(([r, q]) => {
    state[[r, q]] = 0;
    elems[[r, q]] = null;
  });
  
  updateSource(out, dla);

  svg.appendChild(
    svgHexGrid(N, (e, r, q) => {
      console.log("click", r, q);
      
      updateSource(out, dla);

      elems[[r, q]] = svgToken(r, q, SIZE, redPlayer);
      
      if (elems[[r, q]] !== null) {
        svg.appendChild(elems[[r, q]]);
      }
    }, SIZE)
  );
}


main();
