import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { ArticleCardComponent } from './shared/article-card/article-card.component';
import { ArticleHubComponent } from './features/article-hub/article-hub.component';
import { PredictedInsightsComponent } from './shared/predicted-insights/predicted-insights.component';
import { SentimentFilterComponent } from './shared/sentiment-filter/sentiment-filter.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ArticleCardComponent,
    ArticleHubComponent,
    PredictedInsightsComponent,
    SentimentFilterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
