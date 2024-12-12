$(document).ready(function() {
    const $flashcards = $('.flashcard');
    const $underpart =$('.underpart');
    let currentIndex = 0;
    let colorStatus = 0;

    function showFlashcard(index) {
        $flashcards.addClass('hidden'); // すべてのカードを隠す
        $flashcards.eq(index).removeClass('hidden'); // 現在のカードを表示
        $flashcards.eq(index).css('transform', 'translateX(0px)'); // スライド位置をリセット
    }

    function slideToNextCard() {
        const nextIndex = (currentIndex + 1) % $flashcards.length;
        $flashcards.eq(currentIndex).css('transform', 'translateX(-100%)'); // 現在のカードを左にスライド
        $flashcards.eq(nextIndex).css('transform', 'translateX(100%)'); // 次のカードを右からスライド

        setTimeout(() => {
            $flashcards.eq(currentIndex).addClass('hidden'); // 前のカードを非表示にする
        }, 400); // スライドのアニメーションが終わった後に前のカードを非表示にする

        setTimeout(() => {
            $flashcards.eq(nextIndex).removeClass('hidden')
            $flashcards.eq(nextIndex).css('transform', 'translateX(0px)'); // 次のカードを表示
            currentIndex = nextIndex; // インデックスを更新
        }, 400); // スライドの時間と一致させる
    }
    
    showFlashcard(currentIndex);

    $('.upperpart').click(function() {
        slideToNextCard();
        $underpart.addClass('graystatus');
        colorStatus = 0;
    });

    $('.underpart').click(function() {
        if (colorStatus==0){
            $underpart.removeClass('graystatus');
            colorStatus += 1 ;
        }else{
            slideToNextCard();
            $underpart.addClass('graystatus');
            colorStatus = 0;
        }
    });
});