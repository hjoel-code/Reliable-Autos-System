let years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020','2021'];

let yearMininit = $('#search-year-min').html()
let yearMaxinit = $('#search-year-max').html()

function makeOption(option) {
    let optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.innerHTML = option;

    return optionElement;
}

function setYearMin(years) {
    var selectYearMin = document.getElementById('search-year-min');
    selectYearMin.innerHTML = yearMininit;

    years.forEach(year => {
        if ($('#search-year-max').val() === 99999) {
            selectYearMin.appendChild(makeOption(year))
        } else if ($('#search-year-max').val() >= year) {
            selectYearMin.appendChild(makeOption(year))
        }
    })
}

function setYearMax(years) {
    var selectYearMax = document.getElementById('search-year-max');
    selectYearMax.innerHTML = yearMaxinit;

    years.forEach(year => {
        if ($('#select-year-min').val() === 0) {
            selectYearMax.appendChild(makeOption(year))
        } else if ($('#search-year-min').val() <= year) {
            selectYearMax.appendChild(makeOption(year))
        }
    })
}


setYearMin(years);
setYearMax(years);
