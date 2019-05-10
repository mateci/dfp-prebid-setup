import logging

from googleads import ad_manager

from dfp.client import get_client

logger = logging.getLogger(__name__)

def get_line_item_by_name(line_item_name):
  """
  Gets an line_item by name from DFP.

  Args:
    line_item_name (str): the name of the DFP line item
  Returns:
    a DFP line item, or None
  """

  dfp_client = get_client()
  line_item_service = dfp_client.GetService('LineItemService', version='v201811')

  # Filter by name.
  query = 'WHERE name = :name'
  values = [{
    'key': 'name',
    'value': {
      'xsi_type': 'TextValue',
      'value': line_item_name
    }
  }]
  statement = ad_manager.FilterStatement(query, values)
  response = line_item_service.getLineItemsByStatement(statement.ToStatement())

  no_line_item_found = False
  try:
    no_line_item_found = True if len(response['results']) < 1 else False 
  except (AttributeError, KeyError):
    no_line_item_found = True

  if no_line_item_found:
    return None
  else:
    line_item = response['results'][0]
    logger.info(u'Found a line_item with name "{name}".'.format(name=line_item['name']))
    return line_item
