### Requirements
- [x] Login Registration With Validations
- [x] all new `Doggo`s are defaulted to bad boys
  - `Doggo` should have following fields:
    - name
    - profile_pic_url
    - bio
    - age
    - weight
    - tricks
    - is_good_boy
    - birthday
    - created_at
    - updated_at
  - [x] doggos start out displayed in a table of bad boys
- [x] User can add their pet doggos to the app with a url to an image of the dog to be displayed
- [x] redirect to new doggo's page after creation
- [x] click a link to tell the doggo he is a good boy which will filter him out of the bad boy table and into the good boy table
- [x] click a link to tell the doggo he is a bad boy which will filter him out of the good boy table and into the bad boy table
- [x] delete & edit: only the user that added the doggo can edit and delete the doggo
- [x] prefill the edit doggo form with the current data
- [x] display the tricks a doggo can do on the doggos details page: comma separated with no trailing comma
  - start out as a CharField at first, then switch to a relationship so that same tricks are stored only once in a db and associated to every `Doggo` that can do the trick

### Extras
- [ ] doggo can be put up for adoption and another user can adopt the doggo
- [ ] breed relationship, what type of relationship? Even a mixed breed has single name sometimes, such as Puggle which is Beagle and Pug mixed