import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

import { HttpClientModule } from '@angular/common/http';
import { Apollo, gql, APOLLO_OPTIONS } from 'apollo-angular';
import { InMemoryCache, ApolloClient } from '@apollo/client/core';
import {  HttpLink } from 'apollo-angular/http';
import { CommonModule } from '@angular/common';
import { News } from './news';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButton, MatButtonModule } from '@angular/material/button';
import { NavComponent } from './nav/nav.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { HomeComponent } from './home/home.component';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';
import { SearchComponent } from './search/search.component';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { TestComponent } from './test/test.component';
import { NewsComponent } from './news/news.component';
// import { GraphQLModule } from './graphql.module'

@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    HomeComponent,
    SearchComponent,
    NewsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    LayoutModule,
    MatToolbarModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    MatInputModule,
    MatSelectModule,
    MatRadioModule,
    ReactiveFormsModule,
    BrowserModule,
    HttpClientModule,
    FormsModule,
    CommonModule,
    RouterModule.forRoot([
      {path: '', redirectTo: '', pathMatch: 'full' },
      {path:'search',component:SearchComponent},
      {path:'home', component:HomeComponent},
      {path:'news',component:NewsComponent},
      {path:'nav',component:NavComponent},
    ])
    
    

  ],
  providers: [
    {
      provide: APOLLO_OPTIONS,
      useFactory(httpLink: HttpLink){
        return{
          cache: new InMemoryCache(),
          link: httpLink.create({
            uri: 'http://127.0.0.1:8000/graphql/',
          }),
        };
      },
      deps:[HttpLink],
    },
  ],
  bootstrap: [AppComponent]
})
//dependecie injection in angular
export class AppModule {}
