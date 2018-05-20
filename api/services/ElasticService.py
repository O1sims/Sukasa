#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:44:59 2018

@author: owen
"""

from api import config

from elasticsearch import Elasticsearch


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
                if element['property_id'] is None:
                    continue
                else:
                    elastic_response = self.es.index(
                        index=index,
                        doc_type=doc_type,
                        id=element['property_id'],
                        body=element)
        else:
            elastic_response = self.es.index(
                index=index,
                doc_type=doc_type,
                id=data['property_id'],
                body=data)
        return elastic_response
            
    def get_from_database(self, index, doc_type, elastic_id):
        elastic_response = self.es.get(
            index=index, 
            doc_type=doc_type, 
            id=elastic_id)
        return elastic_response['_source']
        
    def search_database(self, index, query_string):
        elastic_response = self.es.search(
            index=index,
            body={"query": query_string})
        search_results = []
        for hit in elastic_response['hits']['hits']:
            search_results.append(hit['_source'])
        return search_results
    
    def count_database(self, index, query_string):
        elastic_response = self.es.count(
            index=index,
            body={"query": query_string})
        return elastic_response['count']
