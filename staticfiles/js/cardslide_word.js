$(document).ready(function() {
    const $flashcards = $('.flashcard');
    const $upperpart =$('.upperpart');
    const $underpart1 =$('.underpart.mean1');
    const $underpart2 =$('.underpart.mean2');

    let currentIndex = 0;
    let phaseStatus = 0;
    const staticPath = "{% static 'images/test_image1.webp' %}";
    

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


    function slideToPreviousCard() {
        console.log(currentIndex);
        if (currentIndex >=1){
        const preIndex = (currentIndex - 1) % $flashcards.length;
        $flashcards.eq(currentIndex).css('transform', 'translateX(100%)'); // 現在のカードを右にスライド
        $flashcards.eq(preIndex).css('transform', 'translateX(-100%)'); // 次のカードを左からスライド

        setTimeout(() => {
            $flashcards.eq(currentIndex).addClass('hidden'); // 前のカードを非表示にする
        }, 600); // スライドのアニメーションが終わった後に前のカードを非表示にする

        setTimeout(() => {
            $flashcards.eq(preIndex).removeClass('hidden')
            $flashcards.eq(preIndex).css('transform', 'translateX(0px)'); // 次のカードを表示
            currentIndex = preIndex; // インデックスを更新
        }, 600); // スライドの時間と一致させる
    }
    }
    
    showFlashcard(currentIndex);

    $('.left-upper').click(function() 
    {
        slideToPreviousCard();
        $upperpart.attr('class', 'upperpart p1');
        $underpart1.attr('class', 'underpart mean1 p1');
        $underpart2.attr('class', 'underpart mean2 p1');
        $('.underpart img').attr('class', 'gray2')
        $('.underpart span').attr('class','gray1');
        phaseStatus = 0;
    });

    $('.right-upper').click(function() 
    {
        slideToNextCard();
        $upperpart.attr('class', 'upperpart p1');
        $underpart1.attr('class', 'underpart mean1 p1');
        $underpart2.attr('class', 'underpart mean2 p1');
        $('.underpart img').attr('class', 'gray2')
        $('.underpart span').attr('class','gray1');
        phaseStatus = 0;
    });



    $('.right-under').click(function() {
        if (phaseStatus==0){
            console.log($underpart1)
    
            $upperpart.removeClass('p1');
            $underpart1.removeClass('p1');
            $underpart2.removeClass('p1');
            $('.underpart img').removeClass('gray2')

            $upperpart.addClass('p2');
            $underpart1.addClass('p2');
            $underpart2.addClass('p2');
            // $underpart1.append(`<img src=${imagePath} class="image"/>`);

            // console.log($underpart1.html());
            // console.log(staticPath)
            // console.log($underpart1)
            // console.log($underpart1.length)

            phaseStatus += 1 ;

        }else if(phaseStatus==1){
            $upperpart.removeClass('p2');
            $underpart1.removeClass('p2');
            $underpart2.removeClass('p2');
            $('.underpart span').removeClass('gray1');

            $upperpart.addClass('p3');
            $underpart1.addClass('p3');
            $underpart2.addClass('p3');
            $('.underpart img').addClass('gray2');

            // $underpart1.find('.image').remove();
        
            phaseStatus += 1 ;

        }else if(phaseStatus==2){
            slideToNextCard();
            $upperpart.attr('class', 'upperpart p1');
            $underpart1.attr('class', 'underpart mean1 p1');
            $underpart2.attr('class', 'underpart mean2 p1');
            $('.underpart span').attr('class','gray1');
            $('.underpart img').attr('class','gray2');

            phaseStatus = 0;
        }

    });

    $('.left-under').click(function() {
        if (phaseStatus==0){
            console.log($underpart1)
    
            $upperpart.removeClass('p1');
            $underpart1.removeClass('p1');
            $underpart2.removeClass('p1');
            $('.underpart img').removeClass('gray2')

            $upperpart.addClass('p2');
            $underpart1.addClass('p2');
            $underpart2.addClass('p2');
            // $underpart1.append(`<img src=${imagePath} class="image"/>`);

            // console.log($underpart1.html());
            // console.log(staticPath)
            // console.log($underpart1)
            // console.log($underpart1.length)

            phaseStatus += 1 ;

        }else if(phaseStatus==1){
            $upperpart.removeClass('p2');
            $underpart1.removeClass('p2');
            $underpart2.removeClass('p2');

            $upperpart.addClass('p1');
            $underpart1.addClass('p1');
            $underpart2.addClass('p1');
            $('.underpart img').addClass('gray2');

            // $underpart1.find('.image').remove();
        
            phaseStatus -= 1 ;

        }else if(phaseStatus==2){

            $upperpart.removeClass('p3');
            $underpart1.removeClass('p3');
            $underpart2.removeClass('p3');
            $('.underpart img').removeClass('gray2')

            $upperpart.addClass('p2');
            $underpart1.addClass('p2');
            $underpart2.addClass('p2');
            $('.underpart span').addClass('gray1')

            phaseStatus -= 1 ;

        }

    });


});