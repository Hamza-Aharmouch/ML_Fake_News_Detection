import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { HttpLink, InMemoryCache } from '@apollo/client/core';
import { Apollo } from "apollo-angular";
import gql from "graphql-tag";
import { Subscription, Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';

//importing service
import {  AllNewsGQL } from '../news.service';


const GET_ALL_NEWS = gql`query GetPostSearch($val: String!){
  allPostDocuments(search:{title:{value: $val}}) {
    edges{
      node{
        id
        title
        details
      }
    }
  }
}`

export interface News {
  id: string;
  title: string;
  details: string;
}
export interface GetMyNews {
  allPostDocuments:{
    edges:[{
      node : News[];
    }];
  };
}


@Injectable({
  providedIn: 'root',
})


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  hasUnitNumber = false;
  @Input() search:string='';
  clearInProgress= false;
  newss: any ;
  loading=true;
  //filteredNews:any;
  constructor(private apollo: Apollo) {}

  ngOnInit():void {

  }

  div1:boolean=false;


  onSubmit() {
    this.apollo.watchQuery<GetMyNews>({
      query: GET_ALL_NEWS,
      variables:{
        val : this.search,
      },
    }).valueChanges.subscribe(
      
        ({ data, loading }) => {
        console.log(loading);
        console.log("success");
        this.newss = data.allPostDocuments.edges;
        console.log(this.newss);
        //this.filteredNews = this.newss;
    });
    
    this.div1=true;
  }
}
