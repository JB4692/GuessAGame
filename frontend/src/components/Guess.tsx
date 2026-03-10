interface Props {
    title: string;
    answer: string | undefined;
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
