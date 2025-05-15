export interface Alert {
    title: string;
    url: string;
    sentiment: string;
    sentiment_score: number;
    topic: string;
    score: number;
    entities: { [key: string]: string[] };
    created_at: string;
  }
  