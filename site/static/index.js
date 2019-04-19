$(document).ready( function() {
    $('.drink').click(function() {
        $('.circle, #drinkProgress').hide();
        $('#drinkImg, #regularBtn, #strongBtn').show();

        imgLoc = $(this).find('img').attr('src');
        drinkName = $(this).find('h5').html();

        $('#drinkImg').attr('src', imgLoc);
        $('#drinkName').html(drinkName);
    });

    $('#regularBtn').click(function() {
        showDrinkProgress('regular');
    });

    $('#strongBtn').click(function() {
        showDrinkProgress('strong');
    });

    $('#saveSettingsBtn').click(function() {
        updateVials();
    });
    
    $('#addDrinkBtn').click(function() {
        addDrink();
    });
});

function showDrinkProgress(strength) {
    $('.circle, #drinkProgress').show();
    $('#drinkImg, #regularBtn, #strongBtn, .close').hide();
    $('#drinkProgress').html('Pouring drink...');

    drink = $('#drinkName').html();
    sendDrinkOrder(drink, strength);

    setTimeout(() => $('#drinkProgress').html('Mixing drink...'), 5000);
    setTimeout(() => $('#drinkProgress').html('Dispensing drink...'), 8000);
    setTimeout(() => $('#drinkProgress').html('Drink Complete!'), 10000);
    setTimeout(() => $('.close').show(), 10000);
}

function sendDrinkOrder(drink, strength) {
    $.ajax({
        url: '/api/makeDrink/' + drink + '/' + strength
    }).done(function(data) {
        strokeTransition();
        increaseNumber();
    });
}

function updateVials() {
    vials = {
        vial1: $('#vial1Input').val(),
        vial2: $('#vial2Input').val(),
        vial3: $('#vial3Input').val(),
        vial4: $('#vial4Input').val(),
        vial5: $('#vial5Input').val(),
        vial6: $('#vial6Input').val()
    }
    
    $.ajax({
        url: '/api/updateVials',
        data: vials
    }).done(function(data) {
        alert('Vials Updated!');
    });
}

function addDrink() {
    ingredients = {};
    ingredients[$('#drinkIngredient1Input').val()] = {
        amount: $('#drinkAmount1Input').val(),
        unit: $('#drinkUnit1Input').val().toLowerCase()
    };
    ingredients[$('#drinkIngredient2Input').val()] = {
        amount: $('#drinkAmount2Input').val(),
        unit: $('#drinkUnit2Input').val().toLowerCase()
    };
    ingredients[$('#drinkIngredient3Input').val()] = {
        amount: $('#drinkAmount3Input').val(),
        unit: $('#drinkUnit3Input').val().toLowerCase()
    };
    
    drink = {
        name: $('#drinkNameInput').val(),
        ingredients: ingredients,
        served: $('#drinkServedInput').val().toLowerCase()
    }
    
    
    $.ajax({
        url: '/api/addDrink',
        data: drink
    }).done(function(data) {
        alert('Drink Added!');
    });
}

function strokeTransition() {
    const transitionDuration = 10000;
    let progress = document.querySelector('.circle__progress--fill');
    let radius = progress.r.baseVal.value;
    let circumference = 2 * Math.PI * radius;

    progress.style.setProperty('--initialStroke', circumference);
    progress.style.setProperty('--transitionDuration', `${transitionDuration}ms`);

    setTimeout(() => progress.style.strokeDashoffset = 0, 100);
}

function increaseNumber() {
    let element = document.querySelector(`.percent__int`),
        interval = 99,
        counter = 0;

    let increaseInterval = setInterval(() => {
        if (counter === 100) { window.clearInterval(increaseInterval); }

        element.textContent = counter;
        counter++;
    }, interval);
}