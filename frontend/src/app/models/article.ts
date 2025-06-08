export interface Article {
    title: string;
    description: string;
    url: string;
    summary: string;
    image_url: string;
    sentiment: string;
    sentiment_score: number;
    topic: string;
    score: number;
    entities: { [key: string]: string[] };
    created_at: string;
}
