import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Article } from '../../models/article';

@Component({
  selector: 'app-article-card',
  templateUrl: './article-card.component.html',
})
export class ArticleCardComponent {
  @Input() article!: Article;

  // Declare outputs so parent can listen to these events
  @Output() viewArticle = new EventEmitter<Article>();
  @Output() predictInsights = new EventEmitter<Article>();

  onView() {
    this.viewArticle.emit(this.article);
  }

  onPredict() {
    this.predictInsights.emit(this.article);
  }

  // Optional if you want to reuse sentiment styling logic here instead of parent
  getSentimentClass(sentiment: string): string {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'text-green-600 font-semibold';
      case 'neutral':
        return 'text-gray-500 font-medium';
      default:
        return 'text-red-500 font-semibold';
    }
  }
}
