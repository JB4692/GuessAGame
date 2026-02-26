interface Props {
    title: string;
    answer: string;
}
const Guess = ({ title, answer }: Props) => {
    let isCorrectAnswer: boolean = title === answer;
    return (
        <div
            className={`guess ${isCorrectAnswer ? "guess-correct" : "guess-wrong"}`}
        >
            {title}
        </div>
    );
};

export default Guess;
