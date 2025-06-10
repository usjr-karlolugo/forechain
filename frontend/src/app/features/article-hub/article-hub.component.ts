import { Component } from '@angular/core';
import { Article } from '../../models/article';
import { ArticleService } from '../../services/article/article.service';
import { PredictService } from '../../services/predict/predict.service';
import { InsightResponse } from '../../models/insight-response';
@Component({
  selector: 'app-article-hub',
  templateUrl: './article-hub.component.html',
  styleUrl: './article-hub.component.css'
})
export class ArticleHubComponent {
  articles: Article[] = [];
  filteredArticles: Article[] = [];
  selectedInsight: string | null = null;
  loading = false;
  hasError = false;
  predictionResult: InsightResponse | null = null;
  errorMessage: string | null = null;
  scrapeUrl: string = '';
  scrapeResult: string | null = null;

  constructor(private articleService: ArticleService, private predictService: PredictService) {}

  ngOnInit() {
    console.log("Getting Articles");
    this.articleService.getArticles().subscribe((data: Article[]) => {
      this.articles = data;
      this.filteredArticles = data;
      console.log("Successfully fetched articles", data);
    });
  }

  filterAccess(sentiment: string){
    console.log('Filters selected', sentiment);
    if (sentiment == 'all'){
      this.filteredArticles = this.articles;
    }else{
      this.filteredArticles = this.articles.filter(article => article.sentiment === sentiment);
    }
  }

  onScrapeArticle(url: string) {
    if (!url || !url.trim()) {
      this.errorMessage = 'Please enter a valid article URL.';
      return;
    }
    this.loading = true;
    this.hasError = false;
    this.errorMessage = null;
    this.predictionResult = null;

    this.predictService.predictInsightsFromUrl(url.trim()).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.loading = false;
      },
      error: (err) => {
        this.hasError = true;
        this.errorMessage = 'Failed to generate prediction from URL.';
        this.loading = false;
        console.error(err);
      }
    });
  }

  onViewArticle(article: Article) {
    console.log('Viewing article:', article);
    if (article.url) {
      window.open(article.url, '_blank');
    } else {
      console.warn('No URL found in article');
    }
  }

  onPredictInsights(article: Article) {
    if (!article.summary) {
      this.errorMessage = 'Summary not available.';
      return;
    }

    this.loading = true;
    this.errorMessage = null;
    this.predictionResult = null;

    this.predictService.predictInsights(article.summary).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Failed to generate prediction.';
        console.error(err);
        this.loading = false;
      }
    });
  }

  getSentimentClass(sentiment: string): string {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'text-green-600 font-semibold';
      case 'negative':
        return 'text-red-500 font-semibold';
      default: 
        return 'text-gray-500 font-medium';
    }
  }
}
