import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { HttpLink, InMemoryCache } from '@apollo/client/core';
import { Apollo } from "apollo-angular";
import gql from "graphql-tag";
import { Subscription, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule} from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
//importing service
import {  AllNewsGQL } from '../news.service';


const GET_ALL_NEWS = gql`query AllNews{ 
  allNews { 
    id 
    title 
    details 
  }
}`

export interface News {
  id: string;
  title: string;
  details: string;
}
export interface GetMyAllNews {
  newss: News[];
}

@Injectable({
  providedIn: 'root',
})


@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent implements OnInit {

  hasUnitNumber = false;
  clearInProgress= false;
  newss: News[] = [];
  loading=true;
  
  constructor(private apollo: Apollo) {}

  ngOnInit(): void {
    this.apollo.watchQuery<any>({
      query: GET_ALL_NEWS
    }).valueChanges.subscribe(

        ({ data, loading }) => {
        console.log(loading);
        console.log('success');
        this.newss = data.allNews;
        console.log(this.newss);
        //this.filteredNews = this.newss;
    });

  }
}
