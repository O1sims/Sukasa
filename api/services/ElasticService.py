#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:44:59 2018

@author: owen
"""

from api import config

from pandas.io.json.normalize import nested_to_record

from elasticsearch import Elasticsearch


def construct_search_query(query, match_all=False):
    """
    @example:
        - "query": { "match": { "address": "mill lane" } }
            Returns all accounts containing the term 'mill' or 'lane' in the address
        - "query": { "match_phrase": { "address": "mill lane" } }
            Returns all accounts containing the phrase 'mill lane' in the address
    :param query:
    :param match_all:
    :return:
    """
    matching_criteria = 'match_phrase' if match_all else 'match'
    return {matching_criteria: query}


class ElasticService:
    def __init__(self):
        self.es = Elasticsearch(
            hosts=[{
                'host': config.ELASTICSEARCH_CONNECTION['host'],
                'port': config.ELASTICSEARCH_CONNECTION['port']
            }])
        
    def save_to_database(self, index, doc_type, data):
        if isinstance(data, list):
            for element in data:
                if element['propertyId'] is None:
                    continue
                else:
                    elastic_response = self.es.index(
                        index=index,
                        doc_type=doc_type,
                        id=element['propertyId'],
                        body=element)
        else:
            elastic_response = self.es.index(
                index=index,
                doc_type=doc_type,
                id=data['propertyId'],
                body=data)
        return elastic_response
            
    def get_from_database(self, index, doc_type, elastic_id):
        elastic_response = self.es.get(
            index=index, 
            doc_type=doc_type, 
            id=elastic_id)
        return elastic_response['_source']
        
    def search_database(self, index, query_dict):
        if not query_dict:
            raise ValueError(
                'Some search criteria are required!')
        query_dict = nested_to_record(
            query_dict,
            sep=".")
        query = construct_search_query(
            query=query_dict)
        elastic_response = self.es.search(
            index=index,
            body={"query": query})
        search_results = []
        for hit in elastic_response['hits']['hits']:
            search_results.append(hit['_source'])
        return search_results

    def drop_database(self, index=None):
        if index is None:
            raise ValueError(
                'Please provide an Elasticserach index')
        else:
            self.es.indices.delete(
                index=index,
                ignore=[400, 404])
    
    def count_database(self, index, query_string):
        elastic_response = self.es.count(
            index=index,
            body={"query": query_string})
        return elastic_response['count']
