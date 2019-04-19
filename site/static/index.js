$(document).ready( function() {
    $('.drink').click(function() {
        $('.circle, #drinkProgress').hide();
        $('#drinkImg, #regularBtn, #strongBtn').show();

        imgLoc = $(this).find('img').attr('src');
        drinkName = $(this).find('h5').html();

        $('#drinkImg').attr('src', imgLoc);
        $('#drinkName').html(drinkName);
    });

    $('#regularBtn, #strongBtn').click(function() {
        $('.circle, #drinkProgress').show();
        $('#drinkImg, #regularBtn, #strongBtn, .close').hide();
        $('#drinkProgress').html('Pouring drink...');
        strokeTransition();
        increaseNumber();

        setTimeout(() => $('#drinkProgress').html('Mixing drink...'), 5000);
        setTimeout(() => $('#drinkProgress').html('Dispensing drink...'), 8000);
        setTimeout(() => $('#drinkProgress').html('Drink Complete!'), 10000);
        setTimeout(() => $('.close').show(), 10000);
    });


})

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
