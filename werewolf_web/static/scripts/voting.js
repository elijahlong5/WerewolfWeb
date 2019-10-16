let timeBetweenRefreshes = 2000;

let GameService = new GameServices();
const access_token = GameService.getAccessTokenFromUrl();
document.addEventListener("DOMContentLoaded", function() {
    let votingDict = window.votingDict;
    console.log(votingDict);
    let countDownDate = new Date(votingDict['exp_time']).getTime();
    // Update the count down every 1 second
    let x = setInterval(function() {
        // Get today's date and time
        let now = new Date().getTime();
        // Find the distance between now and the count down date
        let distance = countDownDate - now;

        // Time calculations for minutes and seconds
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="demo"
        document.getElementById("countdown").innerHTML = minutes + "m " + seconds + "s ";

        // If the count down is over, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "EXPIRED";
        }
    }, 1000);

});