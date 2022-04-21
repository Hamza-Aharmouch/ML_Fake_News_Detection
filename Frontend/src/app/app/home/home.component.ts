import { Component, OnInit, Input} from '@angular/core';
import { map } from 'rxjs/operators';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';
import { APOLLO_OPTIONS } from "apollo-angular";
import { Apollo } from "apollo-angular";
import gql from "graphql-tag";
import { Injectable } from '@angular/core';


const GET_Clean = gql`mutation dataCleaning($val: String!){
  cleanData(textInput: $val){
    data{
      text
    }
  }
}`

const GET_Sentiment = gql`mutation AnalysingData($fel: String!){
  analyseData(textInput: $fel){
    data{
      text
    }
  }
}`

const GET_News_State = gql`mutation detectNews($state: String!){
  detectNews(textInput: $state){
    data{
      text
    }
  }
}`


export interface Data {
  
  text: string;
  
}

export interface GetMyData {
  cleanData:{
    data:Data[];
  };
}

@Injectable({
  providedIn: 'root',
})

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private apollo: Apollo) {}

  ngOnInit(): void {
   
    
  }

  @Input() NLP_Textarea:String='';
  @Input() NewsDetect_Textarea:String='';
  @Input() Sentiment_Textarea:String='';
  NewsDetect_return: any;
  NLP_return: any;
  Sentiment_return: any;

  onclick_NLP(){
    this.apollo.mutate({
      mutation: GET_Clean,
      variables:{
        val : this.NLP_Textarea,
      },
    }).subscribe(
      
        ({ data }) => {
        
        console.log("success");
        console.log(data)
        this.NLP_return = Array.of(data);
        console.log(this.NLP_return);
        //this.filteredNews = this.newss;
    });
    
  }

  onclick_NewsDetect(){
    console.log("process started");
    this.apollo.mutate({
      mutation: GET_News_State,
      variables:{
        state : this.NewsDetect_Textarea,
      },
    }).subscribe(
      
        ({ data }) => {
        
        console.log("success");
        console.log(data)
        this.NewsDetect_return = Array.of(data);
        console.log(this.NewsDetect_return);
        //this.filteredNews = this.newss;
    });
    
    
  }

  onclick_Sentiment(){
    this.apollo.mutate({
      mutation: GET_Sentiment,
      variables:{
        fel : this.Sentiment_Textarea,
      },
    }).subscribe(
      
        ({ data }) => {
        
        console.log("success");
        console.log(data)
        this.Sentiment_return = Array.of(data);
        console.log(this.Sentiment_return);
        //this.filteredNews = this.newss;
    });

  }










  /** Based on the screen size, switch from standard to one column per row */
  // cards = this.breakpointObserver.observe(Breakpoints.Handset).pipe(
  //   map(({ matches }) => {
  //     if (matches) {
  //       return [
  //         { title: 'NLP', cols: 2, rows: 1 },
  //         { title: 'SVM', cols: 2, rows: 1 },
  //         { title: 'Naive Bayes', cols: 2, rows: 1 },
          
  //       ];
  //     }

  //     return [
  //       { title: 'NLP', cols: 2, rows: 1 },
  //       { title: 'SVM', cols: 2, rows: 1 },
  //       { title: 'Naive Bayes', cols: 2, rows: 1 },
        
  //     ];
  //   })
  // );

 
}
