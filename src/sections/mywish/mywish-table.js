import PropTypes from 'prop-types';
import { format } from 'date-fns';
import {
  Avatar,
  Box,
  Card,
  Checkbox,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  Typography
} from '@mui/material';
import { Scrollbar } from 'src/components/scrollbar';
import { getInitials } from 'src/utils/get-initials';

export const MyWishTable = (props) => {
  const {
    count = 0,
    items = [],
    onDeselectAll,
    onDeselectOne,
    onPageChange = () => {},
    onRowsPerPageChange,
    onSelectAll,
    onSelectOne,
    page = 0,
    rowsPerPage = 0,
    selected = []
  } = props;

  const selectedSome = (selected.length > 0) && (selected.length < items.length);
  const selectedAll = (items.length > 0) && (selected.length === items.length);

  return (
    <Card>
      <Scrollbar>
        <Box sx={{ minWidth: 800 }}>
          <Table>
            <TableHead>
              <TableRow>

                <TableCell padding="checkbox">
                  <Checkbox
                    checked={selectedAll}
                    indeterminate={selectedSome}
                    onChange={(event) => {
                      if (event.target.checked) {
                        onSelectAll?.();
                      } else {
                        onDeselectAll?.();
                      }
                    }}
                  />
                </TableCell>

                <TableCell>
                  Producto
                </TableCell>

                <TableCell>
                  Ponderación
                </TableCell> 

                <TableCell>
                  Exclusiones
                </TableCell> 

                <TableCell>
                  Fecha de creación
                </TableCell> 

              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((category) => {
                const isSelected = selected.includes(category.id);

                return (
                  <TableRow
                    hover
                    key={category.id}
                    selected={isSelected}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isSelected}
                        onChange={(event) => {
                          if (event.target.checked) {
                            onSelectOne?.(category.id);
                          } else {
                            onDeselectOne?.(category.id);
                          }
                        }}
                      />
                    </TableCell>

                    <TableCell>
                      <Stack
                        alignItems="center"
                        direction="row"
                        spacing={2}
                      >                        
                        <Typography variant="subtitle2">
                          {category.product_description}
                        </Typography>
                      </Stack>
                    </TableCell>

                    <TableCell>
                      {category.weighting_type}
                    </TableCell>

                    <TableCell>
                      {category.excludes ? (
                        category.excludes.map((exclude) => (
                          <Typography key={exclude} variant="body2">
                            {exclude}
                          </Typography>
                        ))
                      ) : (
                        <Typography variant="body2">No hay exclusiones</Typography>
                      )}
                    </TableCell>

                    <TableCell>
                      {category.created_at}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Box>
      </Scrollbar>
      <TablePagination
        component="div"
        count={count}
        onPageChange={onPageChange}
        onRowsPerPageChange={onRowsPerPageChange}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
};

MyWishTable.propTypes = {
  count: PropTypes.number,
  items: PropTypes.array,
  onDeselectAll: PropTypes.func,
  onDeselectOne: PropTypes.func,
  onPageChange: PropTypes.func,
  onRowsPerPageChange: PropTypes.func,
  onSelectAll: PropTypes.func,
  onSelectOne: PropTypes.func,
  page: PropTypes.number,
  rowsPerPage: PropTypes.number,
  selected: PropTypes.array
};
