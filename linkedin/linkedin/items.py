# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    
    """ 
    Perform a LinkedIn search for people.
    
    :param keywords: Keywords to search on
    :type keywords: str, optional
    :param current_company: A list of company URN IDs (str)
    :type current_company: list, optional
    :param past_companies: A list of company URN IDs (str)
    :type past_companies: list, optional
    :param regions: A list of geo URN IDs (str)
    :type regions: list, optional
    :param industries: A list of industry URN IDs (str)
    :type industries: list, optional
    :param schools: A list of school URN IDs (str)
    :type schools: list, optional
    :param profile_languages: A list of 2-letter language codes (str)
    :type profile_languages: list, optional
    :param contact_interests: A list containing one or both of "proBono" and "boardMember"
    :type contact_interests: list, optional
    :param service_categories: A list of service category URN IDs (str)
    :type service_categories: list, optional
    :param network_depth: Deprecated, use `network_depths`. One of "F", "S" and "O" (first, second and third+ respectively)
    :type network_depth: str, optional
    :param network_depths: A list containing one or many of "F", "S" and "O" (first, second and third+ respectively)
    :type network_depths: list, optional
    :param include_private_profiles: Include private profiles in search results. If False, only public profiles are included. Defaults to False
    :type include_private_profiles: boolean, optional
    :param keyword_first_name: First name
    :type keyword_first_name: str, optional
    :param keyword_last_name: Last name
    :type keyword_last_name: str, optional
    :param keyword_title: Job title
    :type keyword_title: str, optional
    :param keyword_company: Company name
    :type keyword_company: str, optional
    :param keyword_school: School name
    :type keyword_school: str, optional
    :param connection_of: Connection of LinkedIn user, given by profile URN ID
    :type connection_of: str, optional
    :return: List of profiles (minimal data only)
    :rtype: list
    """
    
