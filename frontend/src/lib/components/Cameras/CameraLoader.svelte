<!-- https://uiverse.io/mrhyddenn/calm-snail-67 -->

<div class="loader"></div>

<style>
    .loader {
        width: 75px;
        height: 75px;
        display: inline-block;
        border: 5px solid #14b8a5;
        border-radius: 50%;
        border-top-color: transparent;
        border-bottom-color: transparent;
        animation: rot5 1s infinite;
    }

    @keyframes rot5 {
        0% {
            transform: rotate(0);
        }

        50% {
            transform: rotate(180deg);
            border-top-color: #12a695;
            border-bottom-color: #5accc1;
            border-right-color: transparent;
            border-left-color: transparent;
        }

        100% {
            transform: rotate(360deg);
        }
    }
</style>