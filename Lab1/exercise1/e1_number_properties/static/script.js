function checkPrime() {
    const number = document.getElementById('primeInput').value;
    fetch(`/prime-checker?number=${number}`)
        .then(response => response.json())
        .then(data => document.getElementById('primeResult').innerText = data.result);
}

function calculateGCD() {
    const number1 = document.getElementById('gcdInput1').value;
    const number2 = document.getElementById('gcdInput2').value;
    fetch(`/gcd-calculator?number1=${number1}&number2=${number2}`)
        .then(response => response.json())
        .then(data => document.getElementById('gcdResult').innerText = data.result);
}
