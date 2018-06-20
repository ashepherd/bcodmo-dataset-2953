from datapackage import Package
import sys

if len(sys.argv) != 2:
    raise Exception('This script expects only one parameter: the path to a datapackage.json file')
    sys.exit()

dpkg = sys.argv[1]

print('Reading ' + dpkg)
## Read the created pipeline package
package = Package(dpkg)

for i in range(len(package.resource_names)):
    resource = package.get_resource(package.resource_names[i])
    if (resource.remote is False):
        ## Infer the schema fields
        print('Inferring schema for ' + package.resource_names[i])
        inferred_schema_pkg = Package()
        inferred_schema_pkg.infer(resource.source)
        inferred_resource = inferred_schema_pkg.get_resource(resource.descriptor['name'])
        resource.descriptor['schema'] = inferred_resource.descriptor['schema']
        package.remove_resource(resource.descriptor['name'])
        package.add_resource(resource.descriptor)
        package.commit()
        if (package.valid is not True):
            raise Exception('Package is invalid')
        package.save(dpkg)

