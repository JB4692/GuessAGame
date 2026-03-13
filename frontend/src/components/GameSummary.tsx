interface GameSummaryProps {
    Game: GameData;
}

interface GameData {
    id: number | null;
    gameId: number | null;
    coverUrl: string | null;
    title: string | null;
    genre: string | null;
    platform: string | null;
    releaseDate: number | null;
    summary: string | null;
    rating: number;
}

const GameSummary = ({ Game }: GameSummaryProps) => {
    console.log(Game);
    return (
        <div>
            <h2>Game Info:</h2>
            <p>Genres: {Game.genre}</p>
            <p>Platforms: {Game.platform}</p>
            <p>Release Date: {Game.releaseDate}</p>
            <p>Rating: {Math.trunc(Game.rating)}/100 (From IGDB)</p>
        </div>
    );
};

export default GameSummary;
