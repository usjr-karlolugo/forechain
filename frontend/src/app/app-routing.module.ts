import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ArticleHubComponent } from './features/article-hub/article-hub.component';

const routes: Routes = [
  {path: '', redirectTo: 'article-hub', pathMatch: 'full'},
  {path: 'article-hub', component: ArticleHubComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
