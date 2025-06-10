import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { ArticleCardComponent } from './shared/article-card/article-card.component';
import { ArticleHubComponent } from './features/article-hub/article-hub.component';
import { PredictedInsightsComponent } from './shared/predicted-insights/predicted-insights.component';
import { SentimentFilterComponent } from './shared/sentiment-filter/sentiment-filter.component';
import { UrlInputComponent } from './shared/url-input/url-input.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ArticleCardComponent,
    ArticleHubComponent,
    PredictedInsightsComponent,
    SentimentFilterComponent,
    UrlInputComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
