var words = [
  "baby",
  "doctor",
  "nurse",
  "firefighter",
  "policeman",
  "astronaut",
  "pirate",
  "princess",
  "king",
  "queen",
  "cat",
  "dog",
  "bird",
  "fish",
  "horse",
  "cow",
  "cowboy",
  "pig",
  "sheep",
  "duck",
  "chicken",
  "farmer",
  "chef",
  "scientist",
  "pilot",
  "soldier",
  "athlete",
  "hiker",
  "hulk",
  "diver",
  "skier",
  "surfer",
  "cyclist",
  "runner",
  "ballerina",
  "clown",
  "magician",
  "animal trainer",
  "puppeteer",
  "elmo",
  "santa claus",
  "mime",
  "barney",
  "zombie",
  "ninja",
  "witch",
  "giraffe",
  "vampire",
  "werewolf",
  "ghost",
  "mummy",
  "robot",
  "alien",
  "dinosaur",
  "dragon",
  "running",
  "jumping",
  "dancing",
  "swimming",
  "climbing",
  "flying",
  "rowing",
  "sailing",
  "singing",
  "writing",
  "drawing",
  "painting",
  "cooking",
  "eating",
  "drinking",
  "sleeping",
  "working",
  "shoping",
  "driving",
  "walking",
  "fishing",
  "catching",
  "kicking",
  "fencing",
  "boxing",
  "wrestling",
  "diving",
  "skiing",
  "snowboarding",
  "surfing",
  "snorkeling",
  "sledding",
  "kayaking",
  "grilling",
  "house",
  "apartment",
  "school",
  "hospital",
  "fire station",
  "police station",
  "airport",
  "ship",
  "castle",
  "beach",
  "ocean",
  "mountain",
  "forest",
  "desert",
  "river",
  "lake",
  "park",
  "zoo",
  "aquarium",
  "museum",
  "library",
  "art gallery",
  "music hall",
  "theater",
  "stadium",
  "arena",
  "amusement park",
  "carnival",
  "circus",
  "restaurant",
  "cafe",
  "bakery",
  "supermarket",
  "shopping mall",
  "gas station",
  "car wash",
  "mechanic shop",
  "construction site",
  "factory",
  "bank",
  "hotel",
  "campground",
  "cabin",
  "beach house",
  "ski resort",
  "ice rink",
  "roller rink",
  "golf course",
  "tennis court",
  "basketball court",
  "soccer field",
  "eiffel tower",
  "big ben",
  "statue of liberty",
  "white house",
  "pyramids",
  "great wall of china",
  "taj mahal",
  "golden gate bridge",
  "mount rushmore",
  "grand canyon",
];

function startPopup() {
  const noShow = localStorage.getItem('noShow');
  if (noShow) {
    return;
  }
  else {
    $('#instructionModal').modal('show');
    localStorage.setItem('noShow', true);
  }
}

function showStats(inputData) {
  var totalRight = inputData.slice(0, -1).reduce((partialSum, a) => partialSum + a, 0);
  var total = parseInt(totalRight) + parseInt(inputData.slice(-1));
  statChart.data.datasets[0].data = inputData.slice(0, -1);
  statChart.options.scales.x.title.text = totalRight + "/" + total + " correct (" + (totalRight / Math.max(total, 1) * 100).toFixed(2) + "%)"
  statChart.update();
}

// Checks if mobile device
function isMobileDevice() {
  if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    return true;
  }
  else {
    return false;
  }
};
const ctx = document.getElementById('chart');
var keys = [];
var inputData = [0, 0, 0, 0, 0, 0]
for (var i = 0; i < Object.keys(inputData.slice(0, -1)).length; i++) {
  if (i == 0) {
    keys.push((i + 1) + " guess");
  }
  else {
    keys.push((i + 1) + " guesses");
  }
}
var totalRight = inputData.slice(0, -1).reduce((partialSum, a) => partialSum + a, 0);
var total = parseInt(totalRight) + parseInt(inputData.slice(-1));
Chart.register(ChartDataLabels);
if (isMobileDevice()) {
  Chart.defaults.font.size = 8;
}
else {
  Chart.defaults.font.size = 12;
}
statChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: keys,
    datasets: [{
      data: Object.values(inputData.slice(0, -1)),
      label: " ",
      backgroundColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255, 205, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(54, 162, 235, 1)',
      ]
    }]
  },
  options: {
    aspectRatio: 4,
    layout: {
      padding: {
        left: 10,
        right: 10,
        top: 10,
        bottom: 10,
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip:
      {
        enabled: false,
      },
      datalabels: {
        color: '#ffffff',
      }
    },
    indexAxis: 'y',
    scales: {
      x: {
        ticks: {
          color: '#ffffff',
          display: false,
        },
        title: {
          text: totalRight + "/" + total + " correct (" + (totalRight / Math.max(total, 1) * 100).toFixed(2) + "%)",
          color: '#ffffff',
          display: true,
          font: {
            size: 20,
            weight: 'bold',
          }
        },
        grid: {
          color: '#ffffff',
          display: false,
        },
        beginAtZero: true,
      },
      y: {
        grid: {
          color: '#ffffff',
          display: false,
        },
        ticks: {
          color: '#ffffff'
        },
      }
    },
    responsive: true,
  }
});

function colorize(lists) {
  let result = "Whatsee " + lists.length + "/5\n";
  for (const list of lists) {
    for (const color of list) {
      switch (color.toLowerCase()) {
        case "p":
          result += "🟣 ";
          break;
        case "c":
          result += "🟢 ";
          break;
        case "f":
          result += "🔴 ";
          break;
      }
    }
    result += "\n";
  }
  navigator.clipboard.writeText(result);
  var target = $('#ShareButton')[0];
  const currentLabel = target.innerHTML;
  if (target.innerHTML === 'Copied!') {
    return;
  }
  // Update button label
  target.innerHTML = 'Copied!';

  // Revert button label after 3 seconds
  setTimeout(function () {
    target.innerHTML = currentLabel;
  }, 3000)
}
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function (e) {
    var a, b, i, val = this.value;
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) { return false; }
    currentFocus = -1;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    /*for each item in the array...*/
    var maxItems = 0;
    for (i = 0; i < arr.length; i++) {
      /*check if the item starts with the same letters as the text field value:*/
      if (arr[i].toUpperCase().includes(val.toUpperCase()) && maxItems < 4) {
        maxItems++;
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        var indexOfStr = arr[i].toUpperCase().indexOf(val.toUpperCase());
        /*make the matching letters bold:*/
        b.innerHTML = arr[i].substr(0, indexOfStr);
        b.innerHTML += "<strong>" + arr[i].substr(indexOfStr, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(indexOfStr + val.length);
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function (e) {
          /*insert the value for the autocomplete text field:*/
          inp.value = this.getElementsByTagName("input")[0].value;
          /*close the list of autocompleted values,
          (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function (e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
      increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) { //up
      /*If the arrow UP key is pressed,
      decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 9) { //tab
      console.log("tab");
      closeAllLists();
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}
var inputBoxes = document.getElementsByClassName("myInput");
for (var i of inputBoxes) {
  autocomplete(i, words)
}