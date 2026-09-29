const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const submitBtn =
    document.getElementById("submitBtn");

const clearBtn =
    document.getElementById("clearBtn");

const result =
    document.getElementById("result");

const status =
    document.getElementById("status");


/*
--------------------------------------------------
EXAMPLE PLACEHOLDERS
--------------------------------------------------
*/

const examples = {

    qa:
        "Which is the largest ocean?",

    explain:
        "Explain the Pythagoras theorem in simple words.",

    quiz:
        "Photosynthesis is the process by which green plants use sunlight to make food from carbon dioxide and water.",

    summarize:
        "Paste a long educational paragraph here.",

    learn:
        "SQL"

};


/*
--------------------------------------------------
CHANGE TASK
--------------------------------------------------
*/

task.addEventListener(
    "change",
    () => {

        inputText.placeholder =
            examples[task.value];

        result.innerHTML = "";

        status.textContent = "";

    }
);


/*
--------------------------------------------------
CLEAR
--------------------------------------------------
*/

clearBtn.addEventListener(
    "click",
    () => {

        inputText.value = "";

        result.innerHTML = "";

        status.textContent = "";

    }
);


/*
--------------------------------------------------
HTML ESCAPE
--------------------------------------------------
*/

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


/*
--------------------------------------------------
RENDER QUIZ
--------------------------------------------------
*/

function renderQuiz(quiz) {

    if (!Array.isArray(quiz)) {

        throw new Error(
            "Invalid quiz response."
        );

    }


    result.innerHTML =
        quiz.map(
            (item, index) => `

                <div
                    class="quiz-question"
                    data-index="${index}"
                >

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(
                            item.question
                        )}
                    </h3>

                    <div>

                        ${item.options
                            .map(
                                (
                                    option,
                                    optionIndex
                                ) => `

                                    <button
                                        class="option"
                                        data-option-index="${optionIndex}"
                                    >
                                        ${escapeHtml(
                                            option
                                        )}
                                    </button>

                                `
                            )
                            .join("")
                        }

                    </div>

                    <div
                        class="explanation"
                        hidden
                    ></div>

                </div>

            `
        ).join("");


    /*
    ----------------------------------------------
    QUIZ ANSWER CLICK
    ----------------------------------------------
    */

    result
        .querySelectorAll(
            ".quiz-question"
        )
        .forEach(
            (questionEl, index) => {

                const item =
                    quiz[index];

                questionEl
                    .querySelectorAll(
                        ".option"
                    )
                    .forEach(
                        (button) => {

                            button.addEventListener(
                                "click",
                                () => {

                                    const selected =
                                        button.textContent.trim();


                                    const all =
                                        questionEl
                                            .querySelectorAll(
                                                ".option"
                                            );


                                    all.forEach(
                                        (b) => {

                                            b.disabled =
                                                true;

                                        }
                                    );


                                    if (
                                        selected ===
                                        item.correct_answer
                                    ) {

                                        button.classList.add(
                                            "correct"
                                        );

                                    } else {

                                        button.classList.add(
                                            "wrong"
                                        );


                                        all.forEach(
                                            (b) => {

                                                if (
                                                    b.textContent.trim() ===
                                                    item.correct_answer
                                                ) {

                                                    b.classList.add(
                                                        "correct"
                                                    );

                                                }

                                            }
                                        );

                                    }


                                    const explanation =
                                        questionEl
                                            .querySelector(
                                                ".explanation"
                                            );


                                    explanation.hidden =
                                        false;


                                    if (
                                        selected ===
                                        item.correct_answer
                                    ) {

                                        explanation.textContent =
                                            "Correct! " +
                                            (
                                                item.explanation ||
                                                ""
                                            );

                                    } else {

                                        explanation.textContent =
                                            "Correct answer: " +
                                            item.correct_answer +
                                            ". " +
                                            (
                                                item.explanation ||
                                                ""
                                            );

                                    }

                                }
                            );

                        }
                    );

            }
        );

}


/*
--------------------------------------------------
SUBMIT REQUEST
--------------------------------------------------
*/

async function submit() {

    const text =
        inputText.value.trim();


    if (!text) {

        status.textContent =
            "Please enter some text first.";

        return;

    }


    /*
    Determine endpoint
    */

    let endpoint;


    if (
        task.value ===
        "learn"
    ) {

        endpoint =
            "/learn/recommendations";

    } else {

        endpoint =
            "/" +
            task.value;

    }


    /*
    Request body
    */

    let body;


    if (
        task.value ===
        "quiz"
    ) {

        body = {

            text: text,

            count: 3

        };

    } else {

        body = {

            text: text

        };

    }


    /*
    UI loading state
    */

    submitBtn.disabled =
        true;

    status.textContent =
        "EduGenie is thinking...";

    result.innerHTML =
        "";


    try {

        const response =
            await fetch(
                endpoint,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(body)

                }
            );


        let data;

        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "The server returned an invalid response."
            );

        }


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );

        }


        /*
        Quiz response
        */

        if (
            task.value ===
            "quiz"
        ) {

            renderQuiz(
                data.result
            );

        } else {

            result.textContent =
                data.result;

        }


        status.textContent =
            "Done.";

    } catch (error) {

        status.textContent =
            "Error: " +
            error.message;

    } finally {

        submitBtn.disabled =
            false;

    }

}


/*
--------------------------------------------------
BUTTON CLICK
--------------------------------------------------
*/

submitBtn.addEventListener(
    "click",
    submit
);


/*
--------------------------------------------------
CTRL + ENTER
--------------------------------------------------
*/

inputText.addEventListener(
    "keydown",
    (event) => {

        if (
            (
                event.ctrlKey ||
                event.metaKey
            ) &&
            event.key ===
            "Enter"
        ) {

            submit();

        }

    }
);