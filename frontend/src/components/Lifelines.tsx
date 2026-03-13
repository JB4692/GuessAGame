import rerollImage from "../assets/reroll.png";
import summaryImage from "../assets/summary.png";
import minimapImage from "../assets/map.png";

interface LifelinesProps {
    reroll: () => void;
    rerollCount: number;
    isRerolled: boolean;
    onShowSummary: () => void;
    showSummary: boolean;
}

const Lifelines = ({
    reroll,
    // rerollCount,
    isRerolled,
    onShowSummary,
    showSummary,
}: LifelinesProps) => {
    return (
        <div className="lifelines-container">
            <div>
                <button
                    className={`${!isRerolled ? "" : "btn-used"}`}
                    title="Lifeline: Reroll section"
                    onClick={() => {
                        if (!isRerolled) {
                            reroll();
                        }
                    }}
                >
                    <img src={rerollImage} alt="Reroll" />
                </button>
            </div>
            <button
                className={`${!showSummary ? "" : "btn-used"}`}
                title="Lifeline: Game Info"
                onClick={() => {
                    onShowSummary();
                }}
            >
                <img src={summaryImage} alt="Reroll" />
            </button>
            <button
                title="COMING SOON: Lifeline: Image Minimap"
                onClick={() => {
                    console.log("Clicked minimap!");
                }}
            >
                <img src={minimapImage} alt="Minimap" />
            </button>
        </div>
    );
};

export default Lifelines;
