import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of} from 'rxjs';
import { Article } from '../../models/article';
@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private apiUrl = 'http://127.0.0.1:8000/api/alerts/';

  // private sampleArticles: Article[] = [
  //   {
  //     title: "AI Revolutionizes Healthcare Diagnostics",
  //     description: "AI-driven tools are now diagnosing diseases faster and more accurately than traditional methods.",
  //     url: "https://example.com/ai-healthcare",
  //     sentiment: "Positive",
  //     sentiment_score: 0.92,
  //     topic: "Healthcare",
  //     score: 87,
  //     entities: {
  //       organizations: ["OpenAI", "Mayo Clinic"],
  //       people: ["Dr. Sarah Patel"],
  //       locations: ["United States"]
  //     },
  //     created_at: "2025-05-28T10:15:00Z"
  //   },
  //   {
  //     title: "Stock Markets Dip Amid Global Uncertainty",
  //     description: "Economic instability and geopolitical tensions cause global markets to tumble.",
  //     url: "https://example.com/market-dip",
  //     sentiment: "Negative",
  //     sentiment_score: -0.74,
  //     topic: "Finance",
  //     score: 72,
  //     entities: {
  //       organizations: ["NASDAQ", "World Bank"],
  //       people: ["Janet Yellen"],
  //       locations: ["New York", "Tokyo"]
  //     },
  //     created_at: "2025-05-27T14:30:00Z"
  //   },
  //   {
  //     title: "Neutral Trends in Climate Change Reports",
  //     description: "Recent climate reports suggest a plateau in global temperature rise.",
  //     url: "https://example.com/climate-neutral",
  //     sentiment: "Neutral",
  //     sentiment_score: 0.02,
  //     topic: "Environment",
  //     score: 65,
  //     entities: {
  //       organizations: ["UNEP"],
  //       people: [],
  //       locations: ["Antarctica", "Greenland"]
  //     },
  //     created_at: "2025-05-26T08:45:00Z"
  //   }
  // ];
  
  constructor(private http: HttpClient) { }

  getArticles(): Observable<Article[]> {
    // return of(this.sampleArticles);
    return this.http.get<any[]>(this.apiUrl);
  }
}
