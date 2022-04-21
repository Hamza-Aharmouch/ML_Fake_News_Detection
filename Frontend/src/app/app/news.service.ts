import { Injectable } from '@angular/core';
import { Query, gql } from 'apollo-angular';


export interface News{
  id: string;
  title: string;
  details:string;
}

export interface Response{
  newss:News[];
}


@Injectable({
  providedIn: 'root'
})
export class AllNewsGQL extends Query<Response> {
  document = gql`
  query GetPostSearch($val: String!){
    allPostDocuments(filter:{title:{value: $val}}) {
      edges{
        node{
          id
          title
          details
        }
      }
    }
  }`

  
}
