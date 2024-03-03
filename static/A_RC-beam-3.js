document.addEventListener('DOMContentLoaded', function() {

    document.querySelector(`#rebarOK`).style.display = 'none'
    document.querySelector(`#rebarNotOK`).style.display = 'none'
    document.querySelector(`#shearRebarOK`).style.display = 'none'
    document.querySelector(`#shearRebarNotOK`).style.display = 'none'

});

function checkArea(event) {
    var noOfBars = document.getElementById("numberOfBars");
    var numbervalue = noOfBars.value;
    var diameterOfBars = document.getElementById("diameterOfBars");
    var diaValue = diameterOfBars.value;
    console.log(numbervalue)
    console.log(diaValue)

    var rebarArea = 3.14 * diaValue * diaValue / 4 * numbervalue
    rebarArea= Math.round(rebarArea * 100) / 100

    document.querySelector('#actualTensionRebarArea').value = rebarArea
    requiredArea = document.querySelector('#requiredTensionRebar').value

    if (rebarArea >= requiredArea) {
      document.querySelector(`#rebarOK`).style.display = 'block'
      document.querySelector(`#rebarNotOK`).style.display = 'none'
    }
    else {
      document.querySelector(`#rebarOK`).style.display = 'none'
      document.querySelector(`#rebarNotOK`).style.display = 'block'
    }
};

function checkShearArea(event) {
  var noOfLegs = document.getElementById("numberOfLegs");
  var legvalue = noOfLegs.value;
  var rebarSpacingShear = document.getElementById("rebarSpacing");
  var spacingValue = rebarSpacingShear.value;
  var diameterOfBarsShear = document.getElementById("diameterOfBarsShear");
  var diaShearValue = diameterOfBarsShear.value;

  var elementsPerMeter = 1000 / spacingValue
  var oneShearBarArea = 3.14 * diaShearValue * diaShearValue / 4

  shearRebarArea = oneShearBarArea * elementsPerMeter * legvalue
  shearRebarArea= Math.round(shearRebarArea * 100) / 100

  document.querySelector('#actualShearRebarArea').value = shearRebarArea
  requiredShearArea = document.querySelector('#requiredShearRebar').value

  if (shearRebarArea >= requiredShearArea) {
    document.querySelector(`#shearRebarOK`).style.display = 'block'
    document.querySelector(`#shearRebarNotOK`).style.display = 'none'
  }
  else {
    document.querySelector(`#shearRebarOK`).style.display = 'none'
    document.querySelector(`#shearRebarNotOK`).style.display = 'block'
  }
};

function generatePDF() {
  // Extract information from the form
  var requiredTensionReinforcement = document.getElementById("requiredTensionRebar").value;
  var actualTensionReinforcement = document.getElementById("actualTensionRebarArea").value;
  var numberOfBars = document.getElementById("numberOfBars").value;
  var barDiameter = document.getElementById("diameterOfBars").value;

  var requiredShearReinforcement = document.getElementById("requiredShearRebar").value;
  var actualShearReinforcement = document.getElementById("actualShearRebarArea").value;
  var numberOfLegs = document.getElementById("numberOfLegs").value;
  var stirrupSpacing = document.getElementById("rebarSpacing").value;
  var shearBarDiameter = document.getElementById("diameterOfBarsShear").value;

  // Get the OK / Not OK indicators:
  var rebarOKInput = document.getElementById("rebarOK");
  var rebarNotOKInput = document.getElementById("rebarNotOK");

  if (rebarOKInput.style.display == 'block') {
    // The input is visible, so get its value
    var rebarOKValue = 'PASS';
    console.log("Rebar OK value: " + rebarOKValue);
  }
  if (rebarNotOKInput.style.display == 'block') {
    // The input is visible, so get its value
    var rebarOKValue = 'FAIL';
    console.log("Rebar Not OK value: " + rebarOKValue);
  } else {
    console.log("Rebar OK/NOK input is not visible.");
  }


   // Get the OK / Not OK indicators:
   var shearRebarOKInput = document.getElementById("shearRebarOK");
   var shearRebarNotOKInput = document.getElementById("shearRebarNotOK");

   if (shearRebarOKInput.style.display == 'block') {
     // The input is visible, so get its value
     var shearRebarOKValue = 'PASS';
     console.log("Rebar OK value: " + shearRebarOKValue);
   }
   if (shearRebarNotOKInput.style.display == 'block') {
     // The input is visible, so get its value
     var shearRebarOKValue = 'FAIL';
     console.log("Rebar Not OK value: " + shearRebarOKValue);
   } else {
     console.log("Rebar OK/NOK input is not visible.");
   }



  // Create a HTML template for the PDF content
  var pdfContent = `
    <html>
    <head>
      <style>
        body {
          margin: 20px;
          font-family: Arial, sans-serif;
        }
        h3 {
          color: #333;
        }
        p {
          margin-bottom: 10px;
        }
        .header {
          text-align: center;
          background-color: #eee;
          padding: 10px;
          margin-bottom: 10px;
        }
        }
        .logo-container {
          float: left;
          margin-right: 20px;
        }
        .logo-text-blue {
          color: #537fbe;
        }
        .logo-text-yellow {
          color: #f5b82e;
        }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="logo-container">
          <span class="logo-text-blue">structur</span><span class="logo-text-yellow">AL</span>
        </div>
        <h2>RC Beam Design Information</h2>
      </div>
      <h3>RC beam properties:</h3>
      <p><strong>Beam length:</strong> ${Beam_length} m</p>
      <p><strong>Beam length:</strong> ${Beam_sizeW} mm</p>
      <p><strong>Beam length:</strong> ${Beam_sizeD} mm</p>
      <p><strong>Beam length:</strong> ${concreteClass}</p>
      <p><strong>Beam length:</strong> ${steelClass} MPa</p>
      <p><strong>Reinforcement cover:</strong> bottom: ${coverBottom} mm, top: ${coverTop} mm, sides: ${coverSides} mm" </p>
      <p><strong>Point loads</strong> List of pairs (position [m], magnitude [kN]):</p>
      <p>${pointLoads}</p>
      <p><strong>Distributed loads</strong> List of pairs (start position [m], end position [m], intensity [kN/m]):</p>
      <p>${distributedLoads}</p>
      <br>
      <h3>Static calculation results:</h3>
      <p><strong>Factored Beam Reaction Support A:</strong> ${beamReactionA} kN</p>
      <p><strong>Factored Beam Reaction Support B:</strong> ${beamReactionB} kN</p>
      <p><strong>Beam Maximum Design Bending Moment:</strong> ${beamDesignBM} kNm</p>
      <p><strong>Beam Design Shear Force (Max Positive Value):</strong> ${beamSFpozitive} kN</p>
      <p><strong>Beam Design Shear Force (Max Negative Value):</strong> ${beamSFnegative} kN</p>
      <br>
      <h3>Tension Reinforcement Design:</h3>
      <p><strong>Required Tension Reinforcement:</strong> ${requiredTensionReinforcement} mm²</p>
      <p><strong>Provided Tension Reinforcement Area:</strong> ${actualTensionReinforcement} mm²</p>
      <p><strong>Number of Bars:</strong> ${numberOfBars}</p>
      <p><strong>Bar Diameter:</strong> ${barDiameter}</p>
      <p><strong>Tension Reinforcement Result: <span style="color: blue">${rebarOKValue}</span></strong></p>
      <br>
      <h3>Shear Reinforcement Design:</h3>
      <p><strong>Required Shear Reinforcement:</strong> ${requiredShearReinforcement} mm²/m</p>
      <p><strong>Provided Shear Reinforcement Area:</strong> ${actualShearReinforcement} mm²/m</p>
      <p><strong>Number of Stirrup 'Legs':</strong> ${numberOfLegs}</p>
      <p><strong>Stirrup Spacing:</strong> ${stirrupSpacing}</p>
      <p><strong>Bar Diameter (Shear):</strong> ${shearBarDiameter}</p>
      <p><strong>Shear Reinforcement Result: <span style="color: blue">${shearRebarOKValue}</span></strong></p>
    </body>
    </html>
  `;

  // Use html2pdf library to generate the PDF
  var element = document.createElement("div");
  element.innerHTML = pdfContent;

  // Options for html2pdf
  var options = {
    margin: 20,
    filename: 'beam_reinforcement_design.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };

  html2pdf(element, options);
};
