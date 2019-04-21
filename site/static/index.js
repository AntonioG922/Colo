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
    vial1 = $('#vial1Input').val(),
    vial2 = $('#vial2Input').val(),
    vial3 = $('#vial3Input').val(),
    vial4 = $('#vial4Input').val(),
    vial5 = $('#vial5Input').val(),
    vial6 = $('#vial6Input').val()
    
    if(!vial1 || !vial2 || !vial3 || !vial4 || !vial5 || !vial6) {
        alert('Please fill in all fields');
        return;
    }
    
    $.ajax({
        url: '/api/updateVials/' + vial1 + '/' + vial2 + '/' + vial3 + '/' + vial4 + '/' + vial5 + '/' + vial6
    }).done(function(data) {
        $('#settingsModal').modal('toggle');
        showStatus('Vials Updated');
    });
}

function addDrink() {
    name = $('#drinkNameInput').val();

    ingrdnt1 = $('#drinkIngredient1Input').val();
    ingrdnt1Amount =  $('#drinkAmount1Input').val();
    ingrdnt1Unit = $('#drinkUnit1Input').val().toLowerCase();
    ingrdnt2 = $('#drinkIngredient2Input').val();
    ingrdnt2Amount =  $('#drinkAmount2Input').val();
    ingrdnt2Unit = $('#drinkUnit2Input').val().toLowerCase();
    ingrdnt3 = $('#drinkIngredient3Input').val();
    ingrdnt3Amount =  $('#drinkAmount3Input').val();
    ingrdnt3Unit = $('#drinkUnit3Input').val().toLowerCase();

    served = $('#drinkServedInput').val().toLowerCase();
    
    if(!name || !ingrdnt1 || !ingrdnt1Amount || !ingrdnt2 || !ingrdnt2Amount || !served || (!ingrdnt3 != !ingrdnt3Amount)) {
        alert('Fill in all fields (ingredient 3 optional)');
        return;
    }

    $.ajax({
        url: '/api/addDrink/' + name + '/' + ingrdnt1 + '/' + ingrdnt1Amount + '/' + ingrdnt1Unit + '/' + ingrdnt2 + '/' + ingrdnt2Amount + '/' + ingrdnt2Unit + '/' + (ingrdnt3 ? ingrdnt3 + '/' + ingrdnt3Amount + '/' + ingrdnt3Unit + '/' : '') + served,
    }).done(function(data) {
        $('#addDrinkModal').modal('toggle');
        showStatus(name + ' Added');
    });
}

function showStatus(status) {
    $('#status').css('right', '25px');
    $('#statusText').html(status);
    
    setTimeout(() => $('#status').css('right', '-225px'), 2500)
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
